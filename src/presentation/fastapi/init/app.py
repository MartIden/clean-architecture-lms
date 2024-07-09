from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI

import src
from src.infrastructure.ioc.container.application import AppContainer
from src.infrastructure.settings.stage.app import AppSettings
from src.presentation.fastapi.init.setter.event_handler import EventHandlersSetterFactory
from src.presentation.fastapi.init.setter.exception import ExceptionsHandlerSetterFactory
from src.presentation.fastapi.init.setter.interface import IAppSetter
from src.presentation.fastapi.init.setter.middleware import MiddlewareSetterFactory
from src.presentation.fastapi.init.setter.router import RoutersSetterFactory


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
            RoutersSetterFactory().create(),
        ]

        application = LmsApplication(**self.__app_settings.fastapi_kwargs)

        return application.init(setters)


container = AppContainer()
container.wire(packages=[src])

app_instance = LmsApplicationFactory().create()
