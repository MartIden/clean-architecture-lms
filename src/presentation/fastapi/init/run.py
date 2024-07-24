import asyncio
from abc import ABC, abstractmethod

import uvicorn
from dependency_injector.wiring import Provide, inject

from src.infrastructure.ioc.container.application import AppContainer
from src.infrastructure.settings.stage.app import AppSettings


class IFastApiRunner(ABC):
    @abstractmethod
    def run(self) -> None: ...


class FastApiRunner(IFastApiRunner):

    @inject
    def __init__(self, app_settings: AppSettings = Provide[AppContainer.core.settings]):
        self.__app_settings = app_settings

    def run(self) -> None:
        uvicorn.run(
            "src.presentation.fastapi.init.app:app_instance",
            host=self.__app_settings.HOST,
            port=self.__app_settings.PORT,
            reload=self.__app_settings.RELOAD,
            log_level=self.__app_settings.FASTAPI_LOGGING_LEVEL,
        )


class FastApiRunnerFactory:
    def create(self) -> IFastApiRunner:
        return FastApiRunner()
