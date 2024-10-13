from typing import Optional

from pydantic import UUID4

from src.domain.category.entity.category import Category
from src.domain.category.value_object.value_objects import CategoryTitle, CategoryDescription
from src.domain.common.data_models import JsonModel


class CategoryInCreate(JsonModel):
    title: CategoryTitle
    description: CategoryDescription


class CategoryInUpdate(JsonModel):
    id: UUID4
    title: CategoryTitle | None = None
    description: CategoryDescription | None = None


class CategoryInUpdateRequest(JsonModel):
    title: CategoryTitle | None = None
    description: CategoryDescription | None = None


class CategoryInResponse(JsonModel):
    id: UUID4

    title: CategoryTitle
    description: CategoryDescription

    created_at: int
    updated_at: int

    @classmethod
    def from_entity(cls, entity: Category) -> Optional["CategoryInResponse"]:
        if entity:
            return cls(
                id=entity.id,
                title=entity.title,
                description=entity.description,
                created_at=entity.created_at,
                updated_at=entity.updated_at,
            )
