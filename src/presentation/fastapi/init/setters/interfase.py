from abc import ABC, abstractmethod

from fastapi import FastAPI


class IAppSetter(ABC):
    @abstractmethod
    def set(self, app: FastAPI) -> FastAPI: ...
