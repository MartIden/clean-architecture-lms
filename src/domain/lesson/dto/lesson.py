from typing import Optional

from pydantic import UUID4

from src.domain.common.data_models import JsonModel
from src.domain.common.enum.order import Order
from src.domain.common.value_obj.limit import Limit
from src.domain.lesson.entity.lesson import Lesson
from src.domain.lesson.value_object.cover import LessonCover
from src.domain.lesson.value_object.description import LessonDescription
from src.domain.lesson.value_object.text import LessonContent
from src.domain.lesson.value_object.title import LessonTitle


class LessonInCreate(JsonModel):
    title:       LessonTitle
    description: LessonDescription
    content:     LessonContent
    cover:       LessonCover
    course_id:   UUID4


class LessonInUpdateRequest(JsonModel):
    title:       LessonTitle | None = None
    description: LessonDescription | None = None
    content:     LessonContent | None = None
    cover:       LessonCover | None = None
    course_id:   UUID4 | None = None


class LessonInUpdate(JsonModel):
    id:          UUID4
    title:       LessonTitle | None = None
    description: LessonDescription | None = None
    content:     LessonContent | None = None
    cover:       LessonCover | None = None
    course_id:   UUID4 | None = None


class LessonInResponse(LessonInCreate):
    id: UUID4

    @classmethod
    def from_lesson(cls, lesson: Lesson) -> Optional["LessonInResponse"]:
        if lesson:
            return cls(
                id=lesson.id,
                title=lesson.title,
                description=lesson.description,
                content=lesson.content,
                cover=lesson.cover,
                course_id=lesson.course_id,
            )


class LessonsInResponse(JsonModel):
    rows:  list[LessonInResponse]
    count: int


class LessonManyInRequest(JsonModel):
    limit:  Limit
    offset: int
    order:  Order
