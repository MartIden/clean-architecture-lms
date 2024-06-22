from logging import Logger

from dependency_injector.wiring import Provide

from src.infrastructure.ioc.container.application import AppContainer
from src.infrastructure.settings.stage.app import AppSettings
from src.presentation.rmq.init.declarers.interface import IRmqDeclarer
from src.presentation.rmq.init.migrations.exchanges import IExchangeMigrator


class RmqExchangesDeclarerImpl(IRmqDeclarer):

    def __init__(
        self,
        migrator: IExchangeMigrator,
        app_settings: AppSettings = Provide[AppContainer.core.settings],
        logger: Logger = Provide[AppContainer.core.logger]
    ):
        self.__migrator = migrator
        self._app_settings = app_settings
        self._logger = logger

    async def declare(self) -> None:
        exchanges = self._app_settings.RMQ_MIGRATION_SETTINGS.exchanges

        for exchange in exchanges:
            await self.__migrator.migrate(exchange)
            self._logger.info(f"Declare exchange: {exchange.name}")
