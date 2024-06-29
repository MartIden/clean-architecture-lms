from abc import ABC, abstractmethod
from typing import Sequence

from pydantic import UUID4

from src.domain.user.dto.user import UserInUpdate, UserInCreate
from src.domain.user.entity.user import User
from src.domain.user.exception.user.create import UserCreateError
from src.domain.user.exception.user.exist import UserIsNotExistsError
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
    async def read_by_login(self, login: str) -> User:
        pass

    @abstractmethod
    async def delete(self, id_: UUID4) -> User:
        pass

    @abstractmethod
    async def read_many(self, limit: int, offset: int, order: str, order_by: str) -> list[User]:
        pass

    @abstractmethod
    async def read_by_course_id(
        self, id_: UUID4, limit: int, offset: int, order: str, order_by: str
    ) -> Sequence[User]: ...

    @abstractmethod
    async def count_by_course_id(self, id_: UUID4) -> int: ...

    @abstractmethod
    async def count(self) -> int: ...


class UserCrudService(IUserCrudService):

    def __init__(self, repo: IUserRepo):
        self._repo = repo

    async def create(self, data: UserInCreate) -> User:
        if user := await self._repo.create(data):
            return user
        raise UserCreateError("Не удалось создать пользователя")

    async def update(self, data: UserInUpdate) -> User:
        if user := await self._repo.update(data):
            return user
        raise UserIsNotExistsError(f"Пользователь с id {data.id} не найден")

    async def read_one(self, id_: UUID4) -> User:
        if user := await self._repo.read_one(id_):
            return user
        raise UserIsNotExistsError(f"Пользователь с id {id_} не найден")

    async def delete(self, id_: UUID4) -> User:
        if user := await self._repo.delete(id_):
            return user
        raise UserIsNotExistsError(f"Пользователь с id {id_} не найден")

    async def read_many(self, limit: int, offset: int, order: str, order_by: str) -> Sequence[User]:
        return await self._repo.read_many(limit, offset, order, order_by)

    async def read_by_login(self, login: str) -> User:
        if user := await self._repo.read_by_login(login):
            return user
        raise UserIsNotExistsError(f"Пользователь {login} не найден")

    async def count(self) -> int:
        return await self._repo.count()

    async def read_by_course_id(
        self, id_: UUID4, limit: int, offset: int, order: str, order_by: str
    ) -> Sequence[User]:
        return await self._repo.read_by_course_id(id_, limit, offset, order, order_by)

    async def count_by_course_id(self, id_: UUID4) -> int:
        return await self._repo.count_by_course_id(id_)
