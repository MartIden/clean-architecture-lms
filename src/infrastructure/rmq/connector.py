import asyncio
from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop
from dataclasses import dataclass
from typing import Optional

import aio_pika
from aio_pika import Channel
from aio_pika.abc import AbstractConnection
from aio_pika.pool import Pool
from async_lru import alru_cache


class IRmqConnector(ABC):

    @property
    @abstractmethod
    def _event_loop(self) -> AbstractEventLoop: ...

    @abstractmethod
    async def get_connection(self) -> AbstractConnection: ...

    @abstractmethod
    async def get_single_connection(self) -> AbstractConnection:
        """ function for cache """

    @abstractmethod
    async def get_channel(self) -> Channel:
        """ function for cache """

    @abstractmethod
    async def get_single_channel(self) -> Channel: ...

    @property
    @abstractmethod
    def connection_pool(self) -> Pool[AbstractConnection]: ...

    @property
    @abstractmethod
    def channel_pool(self) -> Pool[Channel]: ...


@dataclass(slots=True, frozen=True)
class RmqConnectionSettings:
    amqp_uri: str
    loop: Optional[AbstractEventLoop] = None
    pool_size = 10
    connection_size = 10
    max_messages_in_parallel = 100


class RmqConnectorImpl(IRmqConnector):

    def __init__(self, connection_settings: RmqConnectionSettings):
        self._uri = connection_settings.amqp_uri
        self._loop = connection_settings.loop
        self._pool_size = connection_settings.pool_size
        self._connection_size = connection_settings.connection_size
        self._max_messages_in_parallel = connection_settings.max_messages_in_parallel

    @property
    def _event_loop(self) -> AbstractEventLoop:
        return self._loop if self._loop else asyncio.get_event_loop()

    async def get_connection(self) -> AbstractConnection:
        return await aio_pika.connect(url=self._uri)

    @alru_cache(maxsize=10)
    async def get_single_connection(self) -> AbstractConnection:
        return await self.get_connection()

    async def get_channel(self) -> Channel:
        async with self.connection_pool.acquire() as connection:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=self._max_messages_in_parallel)
            return channel

    @alru_cache(maxsize=10)
    async def get_single_channel(self) -> Channel:
        async with self.connection_pool.acquire() as connection:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=self._max_messages_in_parallel)
            return channel

    @property
    def connection_pool(self) -> Pool[AbstractConnection]:
        return Pool(self.get_single_connection, max_size=self._connection_size)

    @property
    def channel_pool(self) -> Pool[Channel]:
        return Pool(self.get_channel, max_size=self._pool_size)


class IRmqConnectorFactory(ABC):
    @abstractmethod
    def create(self) -> IRmqConnector: ...