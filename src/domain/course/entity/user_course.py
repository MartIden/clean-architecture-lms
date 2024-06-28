from pydantic import UUID4

from src.domain.common.entity import Entity


class UserCourse(Entity[UUID4]):
    user_id:   UUID4
    course_id: UUID4
