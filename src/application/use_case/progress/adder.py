from abc import ABC, abstractmethod

from pydantic import UUID4

from src.domain.lesson.entity.lesson import Lesson
from src.domain.lesson.exception.exist import LessonIsNotExistsError
from src.domain.lesson.port.lesson_repo import ILessonRepo
from src.domain.progress.dto.progress import ProgressInCreate
from src.domain.progress.entity.progress import Progress
from src.domain.progress.ports.progress_repo import IProgressRepo
from src.domain.user.dto.user import UserSlim


class IProgressAdderCase(ABC):

    @abstractmethod
    async def add(self, lesson_id: UUID4, user: UserSlim) -> Progress: ...


class ProgressAdderCase(IProgressAdderCase):

    def __init__(
        self,
        lesson_repo: ILessonRepo,
        progress_repo: IProgressRepo,
    ):
        self.__lesson_repo = lesson_repo
        self.__progress_repo = progress_repo

    async def add(self, lesson_id: UUID4, user: UserSlim) -> Progress:
        lesson = await self.__lesson_repo.read_one(lesson_id)

        if not lesson:
            raise LessonIsNotExistsError(f"Урок с ID {lesson_id} не найден")

        return await self.__progress_repo.create(
            ProgressInCreate(
                user_id=user.id,
                course_id=lesson.course_id,
                lesson_id=lesson.id,
            )
        )
