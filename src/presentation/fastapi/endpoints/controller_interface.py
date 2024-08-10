from abc import ABC, abstractmethod
from typing import Generic, TypeVar

RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")


class IController(ABC, Generic[RequestT, ResponseT]):
    @abstractmethod
    async def __call__(self, request: RequestT) -> ResponseT: ...
