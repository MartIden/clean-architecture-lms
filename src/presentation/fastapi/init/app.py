from dependency_injector.providers import Factory
from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI

from src.infrastructure.ioc.container.application import AppContainer
from src.infrastructure.settings.stage.app import AppSettings
from src.presentation.fastapi.init.setter.event_handler import EventHandlersSetterFactory
from src.presentation.fastapi.init.setter.exception import ExceptionsHandlerSetterFactory
from src.presentation.fastapi.init.setter.interfase import IAppSetter
from src.presentation.fastapi.init.setter.middleware import MiddlewareSetterFactory


class LmsApplication(FastAPI):
    def init(self, setters: list[IAppSetter]) -> "LmsApplication":
        for setter in setters:
            setter.set(self)
        return self


class LmsApplicationFactory:

    @inject
    def __init__(
        self,
        app_settings: AppSettings = Provide[AppContainer.core.settings],
    ):
        self.__app_settings = app_settings

    def create(self) -> LmsApplication:
        setters = [
            ExceptionsHandlerSetterFactory().create(),
            EventHandlersSetterFactory().create(),
            MiddlewareSetterFactory().create(),
        ]

        application = LmsApplication(**self.__app_settings.fastapi_kwargs)
        return application.init(setters)
