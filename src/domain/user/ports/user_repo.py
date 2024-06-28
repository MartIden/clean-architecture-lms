from abc import ABC, abstractmethod
from typing import Sequence

from pydantic import UUID4

from src.domain.user.dto.user import UserInCreate, UserInUpdate
from src.domain.user.entity.user import User


class IUserRepo(ABC):

    @abstractmethod
    async def create(self, data: UserInCreate) -> User: ...

    @abstractmethod
    async def update(self, data: UserInUpdate) -> User | None: ...

    @abstractmethod
    async def read_one(self, id_: UUID4) -> User | None: ...

    @abstractmethod
    async def delete(self, id_: UUID4) -> User | None: ...

    @abstractmethod
    async def read_many(self, limit: int, offset: int, order: str, order_by: str) -> Sequence[User]: ...

    @abstractmethod
    async def read_by_login(self, login: str) -> User | None: ...

    @abstractmethod
    async def count(self) -> int: ...

    @abstractmethod
    async def read_by_course_id(self, id_: UUID4) -> Sequence[User]: ...
