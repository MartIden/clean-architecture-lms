from pydantic import UUID4

from src.domain.common.entity import Entity
from src.domain.lesson.value_object.cover import LessonCover
from src.domain.lesson.value_object.description import LessonDescription
from src.domain.lesson.value_object.text import LessonContent
from src.domain.lesson.value_object.title import LessonTitle


class Lesson(Entity[UUID4]):

    title: LessonTitle
    description: LessonDescription
    content: LessonContent
    cover: LessonCover
    course_id: UUID4

    @classmethod
    def from_dict(cls, data: dict) -> "Lesson":
        if data:
            return cls(
                id=data.get("id"),
                title=data.get("title"),
                description=data.get("description"),
                text=data.get("text"),
                cover=data.get("cover"),
                course_id=data.get("course_id"),
                created_at=data.get("created_at"),
                updated_at=data.get("updated_at")
            )
