from abc import ABC, abstractmethod

from src.domain.course.dto.course import CourseInUpdate
from src.domain.course.entity.course import Course
from src.domain.course.port.course_repo import ICourseRepo
from src.domain.user.entity.user import User


class ICourseUpdater(ABC):

    @abstractmethod
    async def update(self, data: CourseInUpdate, requested_user: User) -> Course: ...

class CourseUpdater(ICourseUpdater):

    def __init__(self, course_repo: ICourseRepo):
        self.__course_repo = course_repo

    async def update(self, data: CourseInUpdate, requested_user: User) -> Course:
        pass
