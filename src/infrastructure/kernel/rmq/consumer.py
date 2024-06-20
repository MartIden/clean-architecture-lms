from typing import List, Optional, Type
from abc import ABC, abstractmethod
import json

from aio_pika.abc import AbstractIncomingMessage

from src.infrastructure.kernel.ioc.container.application import ApplicationContainer
from src.infrastructure.kernel.rmq.exceptions import NackInterruptException, InterruptException
from src.infrastructure.kernel.rmq.handlers.factory_method import AbstractRmqHandlerCreator
from src.infrastructure.kernel.rmq.handlers.handlers_runner import HandlersRunner


class IRmqConsumer(ABC):

    @abstractmethod
    async def consume(self, no_ack=False, **kwargs):
        pass


class AbstractRmqConsumer(IRmqConsumer, ABC):
    def __init__(self, di_container: ApplicationContainer):
        self._di_container = di_container
        self._logger = self._di_container.core.logger()
        self._connector = self._di_container.infrastructure.rmq_connector()

    @property
    def _auto_ack(self) -> bool:
        return False

    @abstractmethod
    async def _message_handle(self, message: AbstractIncomingMessage):
        """Implement this method to handle incoming messages from consumer"""
        pass

    @property
    @abstractmethod
    def _queue_name(self) -> str:
        pass

    def _logging_message(self, message: str) -> None:
        consumer = type(self).__name__
        extra = {"consumer": consumer, "received_message": message}
        self._logger.info(f"{consumer}: Message received", extra=extra)

    def _message_to_dict(self, message: AbstractIncomingMessage) -> dict:
        body = message.body.decode()
        self._logging_message(body)
        return json.loads(body)

    async def _process_incoming_message(self, message: AbstractIncomingMessage) -> None:
        try:
            await self._message_handle(message)
            await message.ack()
        except NackInterruptException:
            await message.nack(requeue=False)
        except (InterruptException, Exception):
            if self._auto_ack:
                await message.ack()

    async def consume(self, no_ack=False, **kwargs):
        async with self._connector.channel_pool.acquire() as channel:
            queue = await channel.get_queue(self._queue_name)

            await queue.consume(self._process_incoming_message, no_ack=no_ack, **kwargs)

            msg = f"{type(self).__name__} for queue: '{self._queue_name}' has been launched"
            self._logger.info(msg)


class RmqHandlersRunnerConsumerImpl(AbstractRmqConsumer, ABC):

    _handlers_factories: Optional[List[Type[AbstractRmqHandlerCreator]]] = None

    async def _message_handle(self, message: AbstractIncomingMessage):
        try:
            await HandlersRunner(
                self._message_to_dict(message),
                self._handlers_factories,
                self._di_container,
            ).run()
        except json.decoder.JSONDecodeError:
            self._logger.info("The message has an invalid JSON structure")
