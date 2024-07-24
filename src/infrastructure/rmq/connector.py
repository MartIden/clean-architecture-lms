import asyncio
from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop
from dataclasses import dataclass

import aio_pika
from aio_pika import Channel
from aio_pika.abc import AbstractConnection, AbstractChannel
from aio_pika.pool import Pool
from async_lru import alru_cache


class IRmqConnector(ABC):

    @abstractmethod
    async def get_connection(self) -> AbstractConnection: ...

    @abstractmethod
    async def get_cached_connection(self) -> AbstractConnection:
        """ function for cache """

    @abstractmethod
    async def get_channel(self) -> Channel:
        """ function for cache """

    @abstractmethod
    async def get_cached_channel(self) -> Channel: ...

    @property
    @abstractmethod
    def connection_pool(self) -> Pool[AbstractConnection]: ...

    @property
    @abstractmethod
    def channel_pool(self) -> Pool[Channel]: ...


@dataclass(slots=True, frozen=True)
class RmqConnectionSettings:
    amqp_uri: str
    pool_size = 10
    connection_size = 10
    max_messages_in_parallel = 100
    event_loop: AbstractEventLoop | None = None


class RmqConnector(IRmqConnector):

    def __init__(self, connection_settings: RmqConnectionSettings):
        self._uri = connection_settings.amqp_uri
        self._pool_size = connection_settings.pool_size
        self._connection_size = connection_settings.connection_size
        self._max_messages_in_parallel = connection_settings.max_messages_in_parallel
        self._event_loop = connection_settings.event_loop

    @property
    def el(self) -> AbstractEventLoop:
        if self._event_loop:
            return self._event_loop
        return asyncio.get_event_loop()

    async def get_connection(self) -> AbstractConnection:
        return await aio_pika.connect(url=self._uri, loop=self.el)

    @alru_cache(maxsize=1)
    async def get_cached_connection(self) -> AbstractConnection:
        return await self.get_connection()

    @alru_cache(maxsize=1)
    async def get_cached_channel(self) -> AbstractChannel:
        connection = await self.get_cached_connection()
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=self._max_messages_in_parallel)
        return channel

    async def get_channel(self) -> AbstractChannel:
        connection = await self.get_connection()
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=self._max_messages_in_parallel)
        return channel

    @property
    def connection_pool(self) -> Pool[AbstractConnection]:
        return Pool(self.get_connection, max_size=self._connection_size)

    @property
    def channel_pool(self) -> Pool[Channel]:
        return Pool(self.get_channel, max_size=self._pool_size)

    @property
    def cached_channel_pool(self) -> Pool[Channel]:
        return Pool(self.get_cached_channel, max_size=self._pool_size)


class IRmqConnectorFactory(ABC):
    @abstractmethod
    def create(self) -> IRmqConnector: ...
