from abc import ABC, abstractmethod

from asyncio_connection_pool import ConnectionPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker

from src.infrastructure.settings.stage.app import AppSettings


class IPostgresConnectorFactory(ABC):

    @abstractmethod
    def create(self) -> ConnectionPool: ...


class PostgresConnectorFactory(IPostgresConnectorFactory):

    def __init__(self, app_settings: AppSettings):
        self.__app_settings = app_settings

    def create(self) -> async_sessionmaker[AsyncSession]:
        engine = create_async_engine(self.__app_settings.POSTGRES_URI, echo=False)
        return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
