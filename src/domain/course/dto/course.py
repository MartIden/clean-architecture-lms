from typing import Optional

from pydantic import UUID4

from src.domain.common.data_models import JsonModel
from src.domain.common.dto.event import Event
from src.domain.common.enum.order import Order
from src.domain.common.value_obj.limit import Limit
from src.domain.course.entity.course import Course
from src.domain.course.value_object.cover import CourseCover
from src.domain.course.value_object.description import CourseDescription
from src.domain.course.value_object.title import CourseTitle
from src.domain.user.dto.user import UserSlim


class CourseInCreate(JsonModel):
    title:       CourseTitle
    description: CourseDescription
    cover:       CourseCover
    author_id:   UUID4


class CourseInUpdateRequest(JsonModel):
    title:       CourseTitle | None = None
    description: CourseDescription | None = None
    cover:       CourseCover | None = None

    class Config:
        extra = "forbid"


class CourseInUpdateFullRequest(JsonModel):
    title:       CourseTitle | None = None
    description: CourseDescription | None = None
    cover:       CourseCover | None = None
    author_id:   UUID4 | None = None

    class Config:
        extra = "forbid"


class CourseInUpdateEvent(Event):
    id:             UUID4
    title:          CourseTitle | None = None
    description:    CourseDescription | None = None
    cover:          CourseCover | None = None
    author_id:      UUID4 | None = None
    requested_user: UserSlim | None = None


class CourseInUpdate(JsonModel):
    id:          UUID4
    title:       CourseTitle | None = None
    description: CourseDescription | None = None
    cover:       CourseCover | None = None
    author_id:   UUID4 | None = None

    class Config:
        extra = "ignore"


class CourseInResponse(JsonModel):
    id:          UUID4
    title:       CourseTitle
    description: CourseDescription
    cover:       CourseCover
    author_id:   UUID4

    @classmethod
    def from_entity(cls, course: Course) -> Optional["CourseInResponse"]:
        if course:
            return cls(
                id=course.id,
                title=course.title,
                description=course.description,
                cover=course.cover,
                author_id=course.author_id
            )


class CountCoursesInResponse(JsonModel):
    count: int


class CourseByUserManyInRequest(JsonModel):
    id:     UUID4
    limit:  Limit
    offset: int
    order:  Order
