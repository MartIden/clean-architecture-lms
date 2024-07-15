from pydantic import UUID4

from src.domain.common.entity import Entity


class Progress(Entity[UUID4]):
    user_id:   UUID4
    course_id: UUID4
    lesson_id: UUID4

    @classmethod
    def from_dict(cls, data: dict) -> "Progress":
        if data:
            return cls(
                id=data.get("id"),
                login=data.get("user_id"),
                email=data.get("course_id"),
                roles=data.get("lesson_id"),
            )
