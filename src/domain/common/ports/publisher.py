from abc import ABC, abstractmethod
from typing import Optional, Any

from pydantic import BaseModel


class IPublisher(ABC):

    @property
    @abstractmethod
    def publisher_class(self) -> str: ...

    @property
    @abstractmethod
    def _exchange_name(self) -> str | None:
        pass

    @abstractmethod
    async def publish(self, message: str) -> Any:
        pass

    @abstractmethod
    async def publish_model(self, message: BaseModel) -> Any:
        pass

    @abstractmethod
    async def _publish(self, message: bytes) -> Any:
        pass
