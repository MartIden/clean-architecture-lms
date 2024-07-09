from abc import ABC, abstractmethod
from contextlib import asynccontextmanager, AbstractContextManager
from typing import Callable

from asyncio_connection_pool import ConnectionPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker

from src.infrastructure.settings.stage.app import AppSettings


class SessionManager:

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._session_maker = session_maker

    @asynccontextmanager
    async def session(self) -> Callable[..., AbstractContextManager[AsyncSession]]:
        async with self._session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


class IPostgresSessionManagerFactory(ABC):

    @abstractmethod
    def create(self) -> SessionManager: ...


class PostgresSessionManagerFactory(IPostgresSessionManagerFactory):

    def __init__(self, app_settings: AppSettings):
        self.__app_settings = app_settings

    def create(self) -> SessionManager:
        return SessionManager(self.__app_settings.POSTGRES_URI)
