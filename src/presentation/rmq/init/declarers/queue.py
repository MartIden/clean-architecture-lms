from logging import Logger

from dependency_injector.wiring import Provide

from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.rmq.init.migrations.queue import IQueueMigrator
from src.infrastructure.settings.stage.app import AppSettings
from src.presentation.rmq.init.declarers.interface import IRmqDeclarer


class RmqQueuesDeclarerImpl(IRmqDeclarer):
    def __init__(
        self,
        migrator: IQueueMigrator,
        app_settings: AppSettings = Provide[AppContainer.core.settings],
        logger: Logger = Provide[AppContainer.core.logger]
    ):
        self.__migrator = migrator
        self._app_settings = app_settings
        self._logger = logger

    async def declare(self) -> None:
        queues = self._app_settings.RMQ_MIGRATION_SETTINGS.queues

        for queue in queues:
            await self.__migrator.migrate(queue)
            self._logger.info(f"Declare queue: {queue.name}")
