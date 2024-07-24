from typing import Optional

from pydantic import UUID4

from src.domain.common.data_models import JsonModel
from src.domain.common.enum.order import Order
from src.domain.common.value_obj.limit import Limit
from src.domain.progress.entity.progress import Progress


class ProgressInCreate(JsonModel):
    user_id:   UUID4
    course_id: UUID4
    lesson_id: UUID4


class ProgressInUpdateRequest(JsonModel):
    user_id:   UUID4 | None = None
    course_id: UUID4 | None = None
    lesson_id: UUID4 | None = None


class ProgressInUpdate(JsonModel):
    id:       UUID4
    user_id: UUID4 | None = None
    course_id: UUID4 | None = None
    lesson_id: UUID4 | None = None


class ProgressInResponse(JsonModel):
    id:        UUID4
    user_id:   UUID4
    course_id: UUID4
    lesson_id: UUID4

    @classmethod
    def from_entity(cls, entity: Progress) -> Optional["ProgressInResponse"]:
        if entity:
            return cls(
                id=entity.id,
                user_id=entity.user_id,
                course_id=entity.course_id,
                lesson_id=entity.lesson_id
            )


class UsersCountInResponse(JsonModel):
    count: int


class UserByCourseManyInRequest(JsonModel):
    id: UUID4
    limit:  Limit
    offset: int
    order:  Order
