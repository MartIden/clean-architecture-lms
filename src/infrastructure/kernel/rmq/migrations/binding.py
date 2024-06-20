from abc import ABC, abstractmethod

from aio_pika.abc import AbstractExchange, AbstractQueue
from dependency_injector.wiring import inject, Provide

from src.infrastructure.kernel.ioc.container.application import ApplicationContainer
from src.infrastructure.kernel.rmq.connector import IRmqConnector
from src.infrastructure.kernel.settings.unit.rmq_migration import RmqBinding


class IRmqBindingsMigrator(ABC):
    @abstractmethod
    async def migrate(self, binding: RmqBinding) -> None:
        pass


class BaseRmqBindingsMigrator(IRmqBindingsMigrator):
    @inject
    def __init__(self, connector: IRmqConnector = Provide[ApplicationContainer.infrastructure.rmq_connector]):
        self._connector = connector

    async def __get_queue(self, binding: RmqBinding) -> AbstractQueue:
        channel = await self._connector.get_channel()
        return await channel.get_queue(binding.queue)

    async def __get_exchange(self, binding: RmqBinding) -> AbstractExchange:
        channel = await self._connector.get_channel()
        return await channel.get_exchange(binding.exchange)

    async def migrate(self, binding: RmqBinding) -> None:
        queue = await self.__get_queue(binding)
        exchange = await self.__get_exchange(binding)
        await queue.bind(exchange, **binding.kwargs)
