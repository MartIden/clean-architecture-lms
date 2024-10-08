from logging import Logger

from dependency_injector.wiring import Provide, inject

from src.infrastructure.ioc.container.application import AppContainer
from src.infrastructure.settings.stage.app import AppSettings
from src.presentation.rmq.init.declarers.interface import IRmqDeclarer
from src.presentation.rmq.init.migrations.binding import IRmqBindingsMigrator


class RmqBindingsDeclarerImpl(IRmqDeclarer):

    @inject
    def __init__(
        self,
        migrator: IRmqBindingsMigrator,
        app_settings: AppSettings = Provide[AppContainer.core.settings],
        logger: Logger = Provide[AppContainer.core.logger]
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
