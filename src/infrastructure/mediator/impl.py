import traceback
from collections import defaultdict
from logging import Logger

from src.application.use_case.interface import IHandler
from src.domain.common.data_models import ErrorAnswer
from src.domain.common.dto.event import Event, HandlerResult
from src.infrastructure.mediator.interface import IMediator


class Mediator(IMediator):

    def __init__(self, logger: Logger) -> None:
        self.__logger = logger
        self.__registry = defaultdict(list)

    def add_listener(self, event: type[Event], handler: IHandler) -> None:
        self.__registry[event].append(handler)

    def add_listeners(self, rows: tuple[type[Event], IHandler]) -> None:
        for row in rows:
            event, handler = row
            self.add_listener(event, handler)

    async def dispatch(self, event: Event, rise_ex=False) -> dict[type, HandlerResult]:
        results = {}

        handlers = self.__registry.get(type(event), [])

        for handler in handlers:
            status, result, error = True, None, None

            try:
                result = await handler(event)
            except Exception as err:
                if rise_ex:
                    raise

                status = False
                error = ErrorAnswer(
                    error_type=type(err),
                    msg=str(err),
                    traceback=traceback.TracebackException.from_exception(err).format()
                )

            results[type(handler)] = HandlerResult(status=status, value=result, error=error)

        return results

    async def remove_listener(self, event: type[Event]) -> None:
        try:
            del self.__registry[event]
        except IndexError:
            msg = f"Event of {event.__class__.__name__} is not exist in current context"
            self.__logger.error(msg)
            return None
