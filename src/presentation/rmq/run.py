import asyncio
from abc import abstractmethod, ABC

from src.infrastructure.ioc.container.application import ApplicationContainer
from src.presentation.rmq.init.consumer import IRmqConsumer
from src.presentation.rmq.init.migrations.binding import BaseRmqBindingsMigrator
from src.presentation.rmq.init.migrations.exchanges import BaseExchangeMigrator
from src.presentation.rmq.init.migrations.queue import BaseQueueMigrator
from src.presentation.rmq.consumers import get_consumers
from src.presentation.rmq.init.declarers.binding import RmqBindingsDeclarerImpl
from src.presentation.rmq.init.declarers.exchange import RmqExchangesDeclarerImpl
from src.presentation.rmq.init.declarers.interface import IRmqDeclarer
from src.presentation.rmq.init.declarers.queue import RmqQueuesDeclarerImpl


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
