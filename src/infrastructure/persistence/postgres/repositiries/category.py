from pydantic import UUID4

from src.domain.category.dto.category import CategoryInCreate, CategoryInUpdate
from src.domain.category.entity.category import Category
from src.domain.category.port.category_repo import ICategoryRepo
from src.infrastructure.persistence.postgres.repositiries.abstract import AbstractPostgresRepository


class CategoryRepo(AbstractPostgresRepository[UUID4, CategoryInCreate, CategoryInUpdate, Category], ICategoryRepo):

    _result_model = Category

    @property
    def table_name(self) -> str:
        return "categories"
