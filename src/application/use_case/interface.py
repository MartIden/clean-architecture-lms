from abc import ABC, abstractmethod
from typing import TypeVar

from src.domain.common.dto.event import Event, HandlerResult

ResultT = TypeVar("ResultT")


class IHandler[ResultT](ABC):
    @abstractmethod
    async def __call__(self, event: Event) -> HandlerResult: ...
