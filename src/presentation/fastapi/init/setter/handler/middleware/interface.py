from abc import ABC, abstractmethod
from typing import Any

from starlette.middleware import _MiddlewareClass  # noqa


class IMiddlewareHandler(ABC):
    @property
    @abstractmethod
    def middleware_class(self) -> Any: ...

    @property
    @abstractmethod
    def kwargs(self) -> dict: ...
