from abc import ABC, abstractmethod

from pydantic import UUID4

from src.domain.user.dto.user import UserInCreate, UserInUpdate
from src.domain.user.entity.user import User


class IUserRepo(ABC):

    @abstractmethod
    async def create(self, data: UserInCreate) -> User: ...

    @abstractmethod
    async def update(self, data: UserInUpdate) -> User: ...

    @abstractmethod
    async def read_one(self, id_: UUID4) -> User: ...

    @abstractmethod
    async def delete(self, id_: UUID4) -> User: ...

    @abstractmethod
    async def read_many(self, limit: int, offset: int, order: str, order_by: str) -> list[User]: ...
