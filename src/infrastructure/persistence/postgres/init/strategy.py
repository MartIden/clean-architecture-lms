import asyncpg
from asyncio_connection_pool import ConnectionStrategy
from asyncpg import Connection

from src.infrastructure.settings.stage.app import AppSettings


class PostgresStrategy(ConnectionStrategy):

    def __init__(self, settings: AppSettings):
        self.__settings = settings

    async def make_connection(self) -> Connection:
        return await asyncpg.connect(
            dsn=self.__settings.POSTGRES_URI, server_settings={"search_path": self.__settings.POSTGRES_SCHEMA}
        )

    def connection_is_closed(self, conn: Connection) -> bool:
        return conn.is_closed()

    async def close_connection(self, conn: Connection) -> None:
        await conn.close()
