import asyncio
from abc import abstractmethod, ABC
from logging import Logger

from dependency_injector.wiring import Provide

from src.infrastructure.kernel.ioc.container.application import ApplicationContainer
from src.infrastructure.kernel.rmq.consumer import IRmqConsumer
from src.infrastructure.kernel.rmq.migrations.binding import IRmqBindingsMigrator, BaseRmqBindingsMigrator
from src.infrastructure.kernel.rmq.migrations.exchanges import IExchangeMigrator, BaseExchangeMigrator
from src.infrastructure.kernel.rmq.migrations.queue import IQueueMigrator, BaseQueueMigrator
from src.infrastructure.kernel.settings.stage.app import AppSettings
from src.presentation.rmq.consumers import get_consumers


class IRmqDeclarer(ABC):
    @abstractmethod
    async def declare(self) -> None: ...


class RmqExchangesDeclarerImpl(IRmqDeclarer):

    def __init__(
        self,
        migrator: IExchangeMigrator,
        app_settings: AppSettings = Provide[ApplicationContainer.core.settings],
        logger: Logger = Provide[ApplicationContainer.core.logger]
    ):
        self.__migrator = migrator
        self._app_settings = app_settings
        self._logger = logger

    async def declare(self) -> None:
        exchanges = self._app_settings.RMQ_MIGRATION_SETTINGS.exchanges

        for exchange in exchanges:
            await self.__migrator.migrate(exchange)
            self._logger.info(f"Declare exchange: {exchange.name}")


class RmqQueuesDeclarerImpl(IRmqDeclarer):
    def __init__(
        self,
        migrator: IQueueMigrator,
        app_settings: AppSettings = Provide[ApplicationContainer.core.settings],
        logger: Logger = Provide[ApplicationContainer.core.logger]
    ):
        self.__migrator = migrator
        self._app_settings = app_settings
        self._logger = logger

    async def declare(self) -> None:
        queues = self._app_settings.RMQ_MIGRATION_SETTINGS.queues

        for queue in queues:
            await self.__migrator.migrate(queue)
            self._logger.info(f"Declare queue: {queue.name}")


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


class IRmqRunner(ABC):
    @abstractmethod
    async def run(self) -> None: ...


class RmqRunnerImpl(IRmqRunner):

    def __init__(
        self,
        declarers: list[IRmqDeclarer],
        consumers: list[type[IRmqConsumer]],
        di_container: ApplicationContainer
    ):
        self.__declarers = declarers
        self.__consumers = consumers
        self.__di_container = di_container

    async def __run_consumers(self) -> None:
        loop = asyncio.get_running_loop()

        for consumer in self.__consumers:
            rmq_consumer = consumer(self.__di_container)  # noqa
            await loop.create_task(rmq_consumer.consume())

        await asyncio.Future()

    async def run(self) -> None:
        for declarer in self.__declarers:
            await declarer.declare()

        await self.__run_consumers()


class RmqRunnerFactory:
    @classmethod
    def create(cls) -> IRmqRunner:
        container = ApplicationContainer()

        declarers = [
            RmqExchangesDeclarerImpl(migrator=BaseExchangeMigrator()),
            RmqQueuesDeclarerImpl(migrator=BaseQueueMigrator()),
            RmqBindingsDeclarerImpl(migrator=BaseRmqBindingsMigrator()),
        ]

        return RmqRunnerImpl(
            consumers=get_consumers(),
            di_container=container,
            declarers=declarers
        )
