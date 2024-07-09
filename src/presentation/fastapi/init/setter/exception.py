from abc import ABC, abstractmethod
from dataclasses import dataclass
from logging import Logger

from aiohttp import ClientConnectorError
from asyncpg import UniqueViolationError, PostgresError
from dependency_injector.wiring import Provide
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic_core import ValidationError

from src.infrastructure.ioc.container.application import AppContainer
from src.infrastructure.settings.stage.app import AppSettings
from src.presentation.fastapi.init.setter.handler.error_handler.error_400 import Error400Handler
from src.presentation.fastapi.init.setter.handler.error_handler.error_500 import Error500Handler
from src.presentation.fastapi.init.setter.handler.error_handler.interface import IErrorHandler
from src.presentation.fastapi.init.setter.interface import IAppSetter


@dataclass
class FastapiExceptionHandlerMap:
    exception_type: type[Exception]
    handler: IErrorHandler


class ExceptionsHandlerSetter(IAppSetter):

    def __init__(self, exception_handlers_maps: list[FastapiExceptionHandlerMap]):
        self.__exception_handlers_maps = exception_handlers_maps

    def set(self, app: FastAPI) -> FastAPI:
        for exc_handler_map in self.__exception_handlers_maps:
            app.add_exception_handler(exc_handler_map.exception_type, exc_handler_map.handler.handle)
        return app


class IExceptionsHandlerSetterFactory(ABC):
    @abstractmethod
    def create(self) -> IAppSetter: ...


class ExceptionsHandlerSetterFactory(IExceptionsHandlerSetterFactory):

    def __init__(
        self,
        logger: Logger = Provide[AppContainer.core.logger],
        app_settings: AppSettings = Provide[AppContainer.core.settings]
    ):
        self.__logger = logger
        self.__app_settings = app_settings

    def __create_maps(self) -> list[FastapiExceptionHandlerMap]:
        error_500_handler = Error500Handler(self.__app_settings, self.__logger)

        return [
            FastapiExceptionHandlerMap(RequestValidationError, Error400Handler(self.__app_settings, self.__logger)),
            FastapiExceptionHandlerMap(UniqueViolationError, error_500_handler),
            FastapiExceptionHandlerMap(ValidationError, error_500_handler),
            FastapiExceptionHandlerMap(ClientConnectorError, error_500_handler),
            FastapiExceptionHandlerMap(PostgresError, error_500_handler),
            FastapiExceptionHandlerMap(Exception, error_500_handler),
            FastapiExceptionHandlerMap(AttributeError, error_500_handler),
            FastapiExceptionHandlerMap(TypeError, error_500_handler),
            FastapiExceptionHandlerMap(ValueError, error_500_handler),
            FastapiExceptionHandlerMap(IndexError, error_500_handler),
            FastapiExceptionHandlerMap(KeyError, error_500_handler),
            FastapiExceptionHandlerMap(EOFError, error_500_handler),
            FastapiExceptionHandlerMap(ConnectionRefusedError, error_500_handler),
        ]

    def create(self) -> ExceptionsHandlerSetter:
        maps = self.__create_maps()
        return ExceptionsHandlerSetter(maps)
