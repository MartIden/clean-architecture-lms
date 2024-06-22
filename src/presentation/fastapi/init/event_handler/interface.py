from abc import ABC, abstractmethod


class IEventHandler(ABC):

    @property
    @abstractmethod
    def event_type(self) -> str: ...

    @abstractmethod
    async def handle(self) -> None: ...
