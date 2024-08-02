from pydantic import UUID4

from src.domain.category.value_object.value_objects import CategoryTitle, CategoryDescription
from src.domain.common.entity import Entity


class Category(Entity[UUID4]):
    title: CategoryTitle
    description: CategoryDescription
