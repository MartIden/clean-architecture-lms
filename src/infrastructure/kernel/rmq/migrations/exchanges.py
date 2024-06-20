from abc import ABC, abstractmethod

from dependency_injector.wiring import inject, Provide

from src.infrastructure.kernel.ioc.container.application import ApplicationContainer
from src.infrastructure.kernel.rmq.connector import IRmqConnector
from src.infrastructure.kernel.settings.unit.rmq_migration import RmqExchange


class IExchangeMigrator(ABC):
    @abstractmethod
    async def migrate(self, queue: RmqExchange) -> None:
        pass


class BaseExchangeMigrator(IExchangeMigrator):

    @inject
    def __init__(self, connector: IRmqConnector = Provide[ApplicationContainer.infrastructure.rmq_connector]):
        self._connector = connector

    async def migrate(self, exchange: RmqExchange) -> None:
        channel = await self._connector.get_channel()
        await channel.declare_exchange(
            exchange.name, exchange.exchange_type, **exchange.kwargs
        )
