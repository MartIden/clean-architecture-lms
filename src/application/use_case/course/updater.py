from src.application.use_case.interface import IHandler
from src.domain.course.dto.course import CourseInUpdateEvent, CourseInUpdate
from src.domain.course.entity.course import Course
from src.domain.course.exception.course.update import CourseUpdateError
from src.domain.course.port.course_repo import ICourseRepo
from src.domain.user.enum.roles import UserRoleEnum


class ICourseUpdaterHandler(IHandler[Course]):

    async def __call__(self, event: CourseInUpdateEvent) -> Course: ...


class CourseUpdaterHandler(ICourseUpdaterHandler):

    def __init__(self, course_repo: ICourseRepo):
        self.__course_repo = course_repo

    async def __call__(self, event: CourseInUpdateEvent) -> Course:
        course = await self.__course_repo.read_one(event.id)

        if not course:
            raise CourseUpdateError(f"Курс с ID {event.id} не существует")

        update_data = CourseInUpdate(**event.model_dump())

        if (
            course.author_id != event.requested_user.id
            and UserRoleEnum.ADMIN not in event.requested_user.roles
        ):
            raise CourseUpdateError("Допускается редактировать только курсы созданные автором")

        return await self.__course_repo.update(update_data)
