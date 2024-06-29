from abc import ABC, abstractmethod

from src.domain.course.dto.course import CourseInUpdateForUpdater
from src.domain.course.entity.course import Course
from src.domain.course.exception.course.update import CourseUpdateError
from src.domain.course.port.course_repo import ICourseRepo


class ICourseUpdaterCase(ABC):

    @abstractmethod
    async def update(self, data: CourseInUpdateForUpdater) -> Course: ...

class CourseUpdaterCase(ICourseUpdaterCase):

    def __init__(self, course_repo: ICourseRepo):
        self.__course_repo = course_repo

    async def update(self, course_in_update: CourseInUpdateForUpdater) -> Course:
        course = await self.__course_repo.read_one(course_in_update.id)
        if course.author_id != course_in_update.requested_user.id:
            raise CourseUpdateError("Допускается редактировать только курсы созданные автором")
        return await self.__course_repo.update(course_in_update)
