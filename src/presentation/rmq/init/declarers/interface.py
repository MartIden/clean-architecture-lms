from abc import abstractmethod, ABC


class IRmqDeclarer(ABC):
    @abstractmethod
    async def declare(self) -> None: ...
