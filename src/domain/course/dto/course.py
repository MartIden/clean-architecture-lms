from typing import Optional

from pydantic import UUID4, Field

from src.domain.common.data_models import JsonModel
from src.domain.common.enum.order import Order
from src.domain.common.value_obj.limit import Limit
from src.domain.course.entity.course import Course
from src.domain.course.value_object.cover import CourseCover
from src.domain.course.value_object.description import CourseDescription
from src.domain.course.value_object.title import CourseTitle


class CourseInCreate(JsonModel):
    title:       CourseTitle
    description: CourseDescription
    cover:       CourseCover


class CourseInUpdateRequest(JsonModel):
    title:       CourseTitle | None = None
    description: CourseDescription | None = None
    cover:       CourseCover | None = None


class CourseInUpdate(JsonModel):
    id:          UUID4
    title:       CourseTitle | None = None
    description: CourseDescription | None = None
    cover:       CourseCover | None = None


class CourseInResponse(JsonModel):
    id:          UUID4
    title:       CourseTitle
    description: CourseDescription
    cover:       CourseCover

    @classmethod
    def from_course(cls, course: Course) -> Optional["CourseInResponse"]:
        if course:
            return cls(
                id=course.id,
                title=course.title,
                description=course.description,
                cover=course.cover
            )


class CoursesInResponse(JsonModel):
    rows:  list[CourseInResponse]
    count: int


class CourseManyInRequest(JsonModel):
    limit:  Limit
    offset: int
    order:  Order
