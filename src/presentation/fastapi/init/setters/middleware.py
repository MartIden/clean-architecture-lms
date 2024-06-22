from abc import ABC, abstractmethod

from fastapi import FastAPI

from src.presentation.fastapi.init.middleware_handler.cors import CorsMiddlewareHandler
from src.presentation.fastapi.init.middleware_handler.interface import IMiddlewareHandler
from src.presentation.fastapi.init.middleware_handler.raw_context import RawContexMiddlewareHandler
from src.presentation.fastapi.init.setters.interfase import IAppSetter


class MiddlewaresSetter(IAppSetter):

    def __init__(self, middleware_handlers: list[IMiddlewareHandler]):
        self.__middleware_handlers = middleware_handlers

    def set(self, app: FastAPI) -> FastAPI:
        for handler in self.__middleware_handlers:
            app.add_middleware(handler.middleware_class, **handler.kwargs)
        return app


class IMiddlewareSetterFactory(ABC):
    @abstractmethod
    def create(self) -> IAppSetter: ...


class MiddlewareSetterFactory(IMiddlewareSetterFactory):
    def create(self) -> MiddlewaresSetter:
        return MiddlewaresSetter(
            [
                RawContexMiddlewareHandler(),
                CorsMiddlewareHandler(),
            ]
        )
