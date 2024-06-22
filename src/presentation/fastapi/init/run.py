from abc import ABC, abstractmethod

import uvicorn
from dependency_injector.wiring import Provide

from src.infrastructure.ioc.container.application import AppContainer
from src.infrastructure.settings.stage.app import AppSettings
from src.presentation.fastapi.init.app import LmsApplicationFactory, LmsApplication


class IFastApiRunner(ABC):
    @abstractmethod
    def run(self) -> None: ...


class FastApiRunner(IFastApiRunner):

    def __init__(self, app: LmsApplication, app_settings: AppSettings = Provide[AppContainer.core.settings]):
        self.__app = app
        self.__app_settings = app_settings

    def run(self) -> None:

        uvicorn.run(
            self.__app,
            host=self.__app_settings.HOST,
            port=self.__app_settings.PORT,
            log_level=self.__app_settings.FASTAPI_LOGGING_LEVEL
        )


class FastApiRunnerFactory:
    def create(self) -> IFastApiRunner:
        app = LmsApplicationFactory().create()
        return FastApiRunner(app)
