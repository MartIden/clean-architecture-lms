import asyncio
import traceback
from abc import ABC
from logging import INFO, Logger
from typing import Any, Optional

from aio_pika import Message
from aio_pika.abc import DeliveryMode
from pydantic import BaseModel

from src.domain.common.ports.publisher import IPublisher
from src.infrastructure.rmq.connector import RmqConnector
from src.infrastructure.settings.stage.app import AppSettings


class AbstractRmqPublisher(IPublisher, ABC):

    def __init__(
        self,
        connector: RmqConnector,
        app_settings: AppSettings,
        logger: Logger,
    ):
        self._connector = connector
        self._app_settings = app_settings
        self._logger = logger

    @property
    def publisher_class(self) -> str:
        return type(self).__name__

    async def _publish(self, message: bytes) -> Any:
        message = Message(message, delivery_mode=DeliveryMode.PERSISTENT)
        async with self._connector.connection_pool.acquire() as connection:
            channel = await connection.channel()
            exchange = await channel.get_exchange(self._exchange_name)
            return await exchange.publish(message, routing_key=self._exchange_name)

    async def publish(self, message: str) -> Any:
        try:
            bytes_message = message.encode("utf-8")
            publish_status = await self._publish(bytes_message)
            self._log_message(message)

            return publish_status
        except Exception as exc:
            self._log_err_message(message, exc)

    async def publish_model(self, message: BaseModel) -> Any:
        bytes_message = message.model_dump_json().encode("utf-8")
        return await self._publish(bytes_message)

    def _log_publisher(
        self,
        *,
        message: Optional[str] = None,
        extra: Optional[dict] = None,
        log_level=INFO,
    ):
        extra["publisher"] = self.publisher_class
        self._logger.log(log_level, message, extra)

    def _log_message(self, message: str) -> None:
        self._log_publisher(
            message=f"Message to '{self._exchange_name}' has been sending",
            extra={"incoming_message": message},
        )

    def _log_err_message(self, message: str, exc: Exception):
        trace = traceback.format_tb(exc.__traceback__)
        extra = {"traceback": trace, "incoming_message": message}
        message = f"Message was not sent to '{self._exchange_name}' due to an error: '{str(exc)}'"
        self._log_publisher(message=message, extra=extra)
