from abc import ABC, abstractmethod

from dependency_injector.wiring import inject, Provide

from src.infrastructure.ioc.container.application import AppContainer
from src.infrastructure.rmq.connector import IRmqConnector
from src.infrastructure.settings.unit.rmq_migration import RmqBinding


class IRmqBindingsMigrator(ABC):
    @abstractmethod
    async def migrate(self, binding: RmqBinding) -> None:
        pass


class BaseRmqBindingsMigrator(IRmqBindingsMigrator):
    @inject
    def __init__(self, connector: IRmqConnector = Provide[AppContainer.infrastructure.rmq_connector]):
        self._connector = connector

    async def migrate(self, binding: RmqBinding) -> None:
        connection = await self._connector.get_connection()
        async with connection.channel() as channel:
            queue = await channel.get_queue(binding.queue)
            exchange = await channel.get_exchange(binding.exchange)
            await queue.bind(exchange, **binding.kwargs)
        await connection.close()
