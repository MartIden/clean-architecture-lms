from abc import ABC, abstractmethod
from typing import Sequence

from pydantic import UUID4

from src.domain.category.dto.category import CategoryInCreate, CategoryInUpdate
from src.domain.category.entity.category import Category
from src.domain.common.enum.order import Order


class ICategoryRepo(ABC):

    @abstractmethod
    async def create(self, data: CategoryInCreate) -> Category: ...

    @abstractmethod
    async def update(self, data: CategoryInUpdate) -> Category: ...

    @abstractmethod
    async def read_one(self, id_: UUID4) -> Category: ...

    @abstractmethod
    async def delete(self, id_: UUID4) -> Category: ...

    @abstractmethod
    async def read_many(self, limit: int, offset: int, order: Order, order_by: str) -> Sequence[Category]: ...

    @abstractmethod
    async def count(self) -> int: ...
