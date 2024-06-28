from abc import ABC, abstractmethod

from pydantic import UUID4

from src.domain.course.dto.user_course import UserCourseInCreate, UserCourseInUpdate
from src.domain.course.entity.user_course import UserCourse


class IUserCourseRepo(ABC):

    @abstractmethod
    async def create(self, data: UserCourseInCreate) -> UserCourse: ...

    @abstractmethod
    async def update(self, data: UserCourseInUpdate) -> UserCourse | None: ...

    @abstractmethod
    async def read_one(self, id_: UUID4) -> UserCourse: ...

    @abstractmethod
    async def delete(self, id_: UUID4) -> UserCourse: ...

    @abstractmethod
    async def read_many(self, limit: int, offset: int, order: str, order_by: str) -> list[UserCourse]: ...

    @abstractmethod
    async def read_by_user_id(self, id_: UUID4) -> list[UserCourse]: ...

    @abstractmethod
    async def count_by_user_id(self, id_: UUID4) -> int: ...

    @abstractmethod
    async def read_by_course_id(self, id_: UUID4) -> list[UserCourse]: ...

    @abstractmethod
    async def count_by_course_id(self, id_: UUID4) -> int: ...

    @abstractmethod
    async def count(self) -> int: ...
