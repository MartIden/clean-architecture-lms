from abc import ABC, abstractmethod
from dataclasses import dataclass

from aiohttp import ClientConnectorError
from asyncpg import UniqueViolationError, PostgresError
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic_core import ValidationError

from src.presentation.fastapi.init.error_handler.error_500 import Error500Handler
from src.presentation.fastapi.init.error_handler.interface import IErrorHandler
from src.presentation.fastapi.init.setters.interfase import IAppSetter


@dataclass
class FastapiExceptionHandlerMap:
    exception_type: type[Exception]
    handler: IErrorHandler


error_500_handler = Error500Handler()

maps = [
    FastapiExceptionHandlerMap(Exception, error_500_handler),
    FastapiExceptionHandlerMap(AttributeError, error_500_handler),
    FastapiExceptionHandlerMap(TypeError, error_500_handler),
    FastapiExceptionHandlerMap(ValueError, error_500_handler),
    FastapiExceptionHandlerMap(IndexError, error_500_handler),
    FastapiExceptionHandlerMap(KeyError, error_500_handler),
    FastapiExceptionHandlerMap(EOFError, error_500_handler),
    FastapiExceptionHandlerMap(ConnectionRefusedError, error_500_handler),
    FastapiExceptionHandlerMap(UniqueViolationError, error_500_handler),
    FastapiExceptionHandlerMap(ValidationError, error_500_handler),
    FastapiExceptionHandlerMap(ClientConnectorError, error_500_handler),
    FastapiExceptionHandlerMap(RequestValidationError, error_500_handler),
    FastapiExceptionHandlerMap(PostgresError, error_500_handler),
]


class ExceptionsHandlerSetter(IAppSetter):

    def __init__(self, exception_handlers_maps: list[FastapiExceptionHandlerMap]):
        self.__exception_handlers_maps = exception_handlers_maps

    def set(self, app: FastAPI) -> FastAPI:
        for exc_handler_map in self.__exception_handlers_maps:
            app.add_exception_handler(exc_handler_map.exception_type, exc_handler_map.handler.handle)  # noqa
        return app


class IExceptionsHandlerSetterFactory(ABC):
    @abstractmethod
    def create(self) -> IAppSetter: ...


class ExceptionsHandlerSetterFactory(IExceptionsHandlerSetterFactory):
    def create(self) -> ExceptionsHandlerSetter:
        return ExceptionsHandlerSetter(maps)
