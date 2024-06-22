from abc import ABC, abstractmethod

from asyncio_connection_pool import ConnectionPool

from src.infrastructure.persistence.postgres.init.strategy import PostgresStrategy
from src.infrastructure.settings.stage.app import AppSettings


class IPostgresConnectorFactory(ABC):

    @abstractmethod
    def create(self) -> ConnectionPool: ...


class PostgresConnectorFactory(IPostgresConnectorFactory):

    def __init__(self, app_settings: AppSettings):
        self.__app_settings = app_settings

    def create(self) -> ConnectionPool:
        return ConnectionPool(
            strategy=PostgresStrategy(self.__app_settings),
            max_size=self.__app_settings.MAX_CONNECTION,
            burst_limit=round(1.3 * self.__app_settings.MAX_CONNECTION),
        )
