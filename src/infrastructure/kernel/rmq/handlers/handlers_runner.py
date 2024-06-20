import traceback
from typing import Any, List, Type, Optional

from pydantic import ValidationError


from src.infrastructure.kernel.ioc.container.application import ApplicationContainer
from src.infrastructure.kernel.rmq.exceptions import SkipHandleException, InterruptException, NackInterruptException
from src.infrastructure.kernel.rmq.handlers.abstract_handler import AbstractRmqHandler
from src.infrastructure.kernel.rmq.handlers.factory_method import AbstractRmqHandlerCreator


class HandlersRunner:
    def __init__(
        self,
        message: Any,
        handlers_factories: List[Type[AbstractRmqHandlerCreator]],
        di_container: ApplicationContainer,
    ):
        self._message = message
        self._handlers_factories = handlers_factories
        self._di_container = di_container
        self._app_settings = self._di_container.core.settings()
        self._logger = self._di_container.core.logger()

    @staticmethod
    def __get_handler_name(handler: AbstractRmqHandler) -> str:
        return type(handler).__name__

    @staticmethod
    def __get_traceback(exc: Exception) -> list[str]:
        return traceback.format_tb(exc.__traceback__)

    def __create_extra(self, handler_name: str, trace: Optional[list[str]] = None) -> dict:
        extra = {
            "handler": handler_name,
            "input_message": self._message,
        }

        if trace:
            extra["traceback"] = trace

        return extra

    def __skip_exception_handler(
        self, handler: AbstractRmqHandler, exc: Exception
    ) -> None:

        handler_name = self.__get_handler_name(handler)
        error_str = str(exc)

        message = (
            f"The handler '{handler_name}' has been "
            f"skipped with message: {error_str}"
        )
        extra = self.__create_extra(handler_name)

        self._logger.info(msg=message, extra=extra)

    def __skip_consumer(self, handler: AbstractRmqHandler, exc: Exception) -> None:
        handler_name = self.__get_handler_name(handler)
        error_str = str(exc)

        message = (
            f"Consumer has been skipped while executing a "
            f"handler '{handler_name}' with message: {error_str}"
        )

        self._logger.info(msg=message, extra={"input_message": self._message})

    def __exception_handler(self, handler: AbstractRmqHandler, exc: Exception):
        handler_name = self.__get_handler_name(handler)
        trace = self.__get_traceback(exc)
        error_str = str(exc)

        message = f"The handler '{handler_name} was stopped with an error: {error_str}"
        extra = self.__create_extra(handler_name, trace)

        self._logger.exception(msg=message, extra=extra)

    def __exception_create_handler(
        self, creator: Type[AbstractRmqHandlerCreator], exc: Exception
    ):

        handler_name = type(creator).__name__
        trace = self.__get_traceback(exc)
        error_str = str(exc)

        message = (
            f"It didn't work to create a handler '{handler_name}'. "
            f"An error occurred while creating the handler: {error_str}"
        )
        extra = self.__create_extra(handler_name, trace)

        self._logger.exception(msg=message, extra=extra)

    def __create_handler(self, handler_factory: Type[AbstractRmqHandlerCreator]):
        try:
            factory = handler_factory(self._message, self._di_container)
            return factory.create()
        except Exception as err:
            self.__exception_create_handler(handler_factory, err)
            return

    async def __handle(self, handler: AbstractRmqHandler) -> None:
        try:
            await handler.handle()
        except SkipHandleException as err:
            self.__skip_exception_handler(handler, err)
        except InterruptException as err:
            self.__skip_consumer(handler, err)
            raise InterruptException
        except NackInterruptException as err:
            self.__exception_handler(handler, err)
            raise NackInterruptException
        except TypeError as err:
            self.__exception_handler(handler, err)
        except ValidationError as err:
            self.__exception_handler(handler, err)
        except Exception as err:
            self.__exception_handler(handler, err)

    async def _run_handler(
        self, handler_factory: Type[AbstractRmqHandlerCreator]
    ) -> None:
        handler = self.__create_handler(handler_factory)
        if handler:
            await self.__handle(handler)

    async def run(self) -> None:
        for handler_factory in self._handlers_factories:
            await self._run_handler(handler_factory)
