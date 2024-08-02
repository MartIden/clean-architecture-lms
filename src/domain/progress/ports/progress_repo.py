from abc import ABC, abstractmethod
from typing import Sequence

from pydantic import UUID4

from src.domain.progress.dto.progress import ProgressInCreate, ProgressInUpdate
from src.domain.progress.entity.progress import Progress


class IProgressRepo(ABC):

    @abstractmethod
    async def create(self, data: ProgressInCreate) -> Progress: ...

    @abstractmethod
    async def update(self, data: ProgressInUpdate) -> Progress | None: ...

    @abstractmethod
    async def read_one(self, id_: UUID4) -> Progress | None: ...

    @abstractmethod
    async def delete(self, id_: UUID4) -> Progress | None: ...

    @abstractmethod
    async def read_many(self, limit: int, offset: int, order: str, order_by: str) -> Sequence[Progress]: ...

    @abstractmethod
    async def count(self) -> int: ...

    @abstractmethod
    async def get_by_course(self, course_id: UUID4, user_id: UUID4) -> Sequence[Progress]: ...
