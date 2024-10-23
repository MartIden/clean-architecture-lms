from abc import ABC

from src.domain.course.dto.course import CourseInUpdateEvent, CourseInUpdate
from src.domain.course.entity.course import Course
from src.domain.course.exception.course.update import CourseUpdateError
from src.domain.course.port.course_repo import ICourseRepo
from src.domain.user.enum.roles import UserRoleEnum


class ICourseUpdaterCase(ABC):

    async def __call__(self, data: CourseInUpdate) -> Course: ...


class CourseUpdaterCase(ICourseUpdaterCase):

    def __init__(self, course_repo: ICourseRepo):
        self.__course_repo = course_repo

    async def __call__(self, data: CourseInUpdateEvent) -> Course:
        course = await self.__course_repo.read_one(data.id)

        if not course:
            raise CourseUpdateError(f"Курс с ID {data.id} не существует")

        update_data = CourseInUpdate(**data.model_dump())

        if (
            course.author_id != data.requested_user.id
            and UserRoleEnum.ADMIN not in data.requested_user.roles
        ):
            raise CourseUpdateError("Допускается редактировать только курсы созданные автором")

        return await self.__course_repo.update(update_data)
