from abc import ABC, abstractmethod
from typing import TypeVar, Any

from src.application.use_case.interface import IHandler
from src.domain.common.dto.event import Event, HandlerResult


class IMediator(ABC):
    @abstractmethod
    def add_listener(self, event: type[Event], handler: IHandler) -> None: ...
    @abstractmethod
    def add_listeners(self, rows: tuple[type[Event], IHandler]) -> None: ...
    @abstractmethod
    async def dispatch(self, event: Event, rise_ex=False) -> dict[type, HandlerResult]: ...
    @abstractmethod
    async def remove_listener(self, event: type[Event]) -> None: ...
