from abc import ABC, abstractmethod

from starlette.requests import Request
from starlette.responses import Response


class IErrorHandler(ABC):

    @property
    @abstractmethod
    def _http_code(self) -> int: ...

    @abstractmethod
    async def handle(self, request: Request, exc: Exception) -> Response: ...
