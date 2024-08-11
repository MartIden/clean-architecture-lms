from abc import ABC, abstractmethod
from typing import TypeVar, Any

from src.application.handler.interface import IHandler
from src.domain.common.dto.event import Event


class IMediator(ABC):
    @abstractmethod
    def add_listener(self, event: type[Event], handler: IHandler) -> None: ...
    @abstractmethod
    def add_listeners(self, rows: tuple[type[Event], IHandler]) -> None: ...
    @abstractmethod
    async def dispatch(self, event: Event) -> Any: ...
    @abstractmethod
    async def remove_listener(self, event: type[Event]) -> None: ...
