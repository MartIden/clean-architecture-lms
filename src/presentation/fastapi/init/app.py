from dependency_injector.wiring import Provide
from fastapi import FastAPI

from src.infrastructure.settings.stage.app import AppSettings
from src.presentation.fastapi.init.setters.interfase import IAppSetter
from src.infrastructure.ioc.container.application import ApplicationContainer
from src.presentation.fastapi.init.setters.event_handler import EventHandlersSetterFactory
from src.presentation.fastapi.init.setters.exception import ExceptionsHandlerSetterFactory
from src.presentation.fastapi.init.setters.middleware import MiddlewareSetterFactory


class LmsApplication(FastAPI):
    def init(self, setters: list[IAppSetter]) -> "LmsApplication":
        for setter in setters:
            setter.set(self)
        return self


class LmsApplicationFactory:
    def __init__(
        self,
        app_settings: AppSettings = Provide[ApplicationContainer.core.settings],
    ):
        self.__app_settings = app_settings

    def create(self) -> LmsApplication:
        setters = [
            ExceptionsHandlerSetterFactory().create(),
            EventHandlersSetterFactory().create(),
            MiddlewareSetterFactory().create(),
        ]

        app = LmsApplication(**self.__app_settings.fastapi_kwargs)
        return app.init(setters)
