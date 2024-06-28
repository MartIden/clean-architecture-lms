from typing import Optional

from pydantic import UUID4

from src.domain.common.data_models import JsonModel
from src.domain.common.enum.order import Order
from src.domain.common.value_obj.limit import Limit
from src.domain.course.entity.user_course import UserCourse


class UserCourseInCreate(JsonModel):
    user_id:   UUID4
    course_id: UUID4


class UserCourseInUpdateRequest(JsonModel):
    user_id:   UUID4 | None = None
    course_id: UUID4 | None = None


class UserCourseInUpdate(JsonModel):
    id:        UUID4
    user_id:   UUID4 | None = None
    course_id: UUID4 | None = None


class UserCourseInResponse(JsonModel):
    id:        UUID4
    user_id:   UUID4 | None = None
    course_id: UUID4 | None = None

    @classmethod
    def from_user_course(cls, user_course: UserCourse) -> Optional["UserCourseInResponse"]:
        if user_course:
            return cls(
                id=user_course.id,
                user_id=user_course.user_id,
                course_id=user_course.course_id,
            )


class UserCoursesInResponse(JsonModel):
    rows:  list[UserCourseInResponse]
    count: int


class UserCourseManyInRequest(JsonModel):
    limit:  Limit
    offset: int
    order:  Order
