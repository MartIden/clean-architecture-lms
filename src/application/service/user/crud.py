from abc import ABC, abstractmethod

from pydantic import UUID4

from src.domain.user.dto.user import UserInUpdate, UserInCreate
from src.domain.user.entity.user import User
from src.domain.user.ports.user_repo import IUserRepo


class IUserCrudService(ABC):
    @abstractmethod
    async def create(self, data: UserInCreate) -> User:
        pass

    @abstractmethod
    async def update(self, data: UserInUpdate) -> User:
        pass

    @abstractmethod
    async def read_one(self, id_: UUID4) -> User:
        pass

    @abstractmethod
    async def delete(self, id_: UUID4) -> User:
        pass

    @abstractmethod
    async def read_many(self, limit: int, offset: int, order: str, order_by: str) -> list[User]:
        pass

    @abstractmethod
    async def count(self) -> int: ...


class UserCrudService(IUserCrudService):

    def __init__(self, repo: IUserRepo):
        self._repo = repo

    async def create(self, data: UserInCreate) -> User:
        return await self._repo.create(data)

    async def update(self, data: UserInUpdate) -> User:
        return await self._repo.update(data)

    async def read_one(self, id_: UUID4) -> User:
        return await self._repo.read_one(id_)

    async def delete(self, id_: UUID4) -> User:
        return await self._repo.delete(id_)

    async def read_many(self, limit: int, offset: int, order: str, order_by: str) -> list[User]:
        return await self._repo.read_many(limit, offset, order, order_by)

    async def count(self) -> int:
        return await self._repo.count()
