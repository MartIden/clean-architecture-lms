from abc import ABC, abstractmethod
from typing import Sequence

from pydantic import UUID4

from src.domain.common.enum.order import Order
from src.domain.lesson.dto.lesson import LessonInCreate, LessonInUpdate
from src.domain.lesson.entity.lesson import Lesson


class ILessonRepo(ABC):
    
    @abstractmethod
    async def create(self, data: LessonInCreate) -> Lesson: ...

    @abstractmethod
    async def update(self, data: LessonInUpdate) -> Lesson: ...

    @abstractmethod
    async def read_one(self, id_: UUID4) -> Lesson: ...

    @abstractmethod
    async def delete(self, id_: UUID4) -> Lesson: ...

    @abstractmethod
    async def read_many(self, limit: int, offset: int, order: Order, order_by: str) -> Sequence[Lesson]: ...

    @abstractmethod
    async def read_by_course(self, id_: UUID4) -> Sequence[Lesson]: ...

    @abstractmethod
    async def count_by_course(self, id_: UUID4) -> int: ...

    @abstractmethod
    async def count(self) -> int: ...
