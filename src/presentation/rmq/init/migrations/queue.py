from abc import ABC, abstractmethod

from dependency_injector.wiring import Provide, inject

from src.infrastructure.ioc.container.application import ApplicationContainer
from src.presentation.rmq.init.connector import IRmqConnector
from src.infrastructure.settings.unit.rmq_migration import RmqQueue


class IQueueMigrator(ABC):
    @abstractmethod
    async def migrate(self, queue: RmqQueue) -> None:
        pass


class BaseQueueMigrator(IQueueMigrator):

    @inject
    def __init__(self, connector: IRmqConnector = Provide[ApplicationContainer.infrastructure.rmq_connector]):
        self._connector = connector

    async def __create_queue(self, queue: RmqQueue) -> None:
        connection = await self._connector.get_single_connection()
        async with connection.channel() as channel:
            await channel.declare_queue(queue.name, **queue.kwargs)

    async def migrate(self, queue: RmqQueue) -> None:
        await self.__create_queue(queue)
