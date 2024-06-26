from abc import ABC, abstractmethod
from typing import Generic, TypeVar

RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")


class IController[RequestT, ResponseT](ABC):
    @abstractmethod
    async def __call__(self, request: RequestT) -> ResponseT: ...
