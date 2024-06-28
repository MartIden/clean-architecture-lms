from pydantic import UUID4

from src.domain.common.entity import Entity
from src.domain.course.value_object.cover import CourseCover
from src.domain.course.value_object.description import CourseDescription
from src.domain.course.value_object.title import CourseTitle


class Course(Entity[UUID4]):

    title:       CourseTitle
    description: CourseDescription
    cover:       CourseCover

    @classmethod
    def from_dict(cls, data: dict) -> "Course":
        if data:
            return cls(
                id=data.get("id"),
                login=data.get("title"),
                email=data.get("description"),
                roles=data.get("cover"),
                password=data.get("password"),
                created_at=data.get("created_at"),
                updated_at=data.get("updated_at")
            )
