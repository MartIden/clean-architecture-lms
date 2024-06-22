from typing import Any

from aio_pika import ExchangeType
from pydantic import BaseModel


class RmqBinding(BaseModel):
    queue: str
    exchange: str
    kwargs: dict[str, Any]


class RmqQueue(BaseModel):
    name: str
    kwargs: dict[str, Any]


class RmqExchange(BaseModel):
    name: str
    exchange_type: ExchangeType
    kwargs: dict[str, Any]


class RmqMigrationSettings(BaseModel):
    queues: list[RmqQueue]
    bindings: list[RmqBinding]
    exchanges: list[RmqExchange]
