from abc import ABC, abstractmethod

from pydantic import UUID4

from src.domain.common.enum.order import Order
from src.domain.course.dto.course import CourseInCreate, CourseInUpdate
from src.domain.course.entity.course import Course


class ICourseRepo(ABC):
    
    @abstractmethod
    async def create(self, data: CourseInCreate) -> Course: ...

    @abstractmethod
    async def update(self, data: CourseInUpdate) -> Course: ...

    @abstractmethod
    async def read_one(self, id_: UUID4) -> Course: ...

    @abstractmethod
    async def delete(self, id_: UUID4) -> Course: ...

    @abstractmethod
    async def read_many(self, limit: int, offset: int, order: Order, order_by: str) -> list[Course]: ...

    @abstractmethod
    async def count(self) -> int: ...
