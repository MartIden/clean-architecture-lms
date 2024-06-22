from logging import Logger

from dependency_injector.wiring import Provide

from src.infrastructure.ioc.container.application import ApplicationContainer
from src.infrastructure.settings.stage.app import AppSettings
from src.presentation.rmq.init.declarers.interface import IRmqDeclarer
from src.presentation.rmq.init.migrations.binding import IRmqBindingsMigrator


class RmqBindingsDeclarerImpl(IRmqDeclarer):

    def __init__(
        self,
        migrator: IRmqBindingsMigrator,
        app_settings: AppSettings = Provide[ApplicationContainer.core.settings],
        logger: Logger = Provide[ApplicationContainer.core.logger]
    ):
        self.__migrator = migrator
        self._app_settings = app_settings
        self._logger = logger

    async def declare(self) -> None:
        bindings = self._app_settings.RMQ_MIGRATION_SETTINGS.bindings

        for binding in bindings:
            await self.__migrator.migrate(binding)
            msg = f"Declare binding from exchange {binding.exchange} to queue {binding.queue}"
            self._logger.info(msg)
