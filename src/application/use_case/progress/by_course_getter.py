from abc import ABC, abstractmethod
from typing import Sequence

from pydantic import UUID4

from src.domain.lesson.port.lesson_repo import ILessonRepo
from src.domain.progress.entity.progress import Progress
from src.domain.progress.ports.progress_repo import IProgressRepo


class IByCourseProgressGetterUseCase(ABC):
    @abstractmethod
    async def get(self, course_id: UUID4, user_id: UUID4) -> tuple[list[Progress], int]: ...


class ByCourseProgressGetterUseCase(IByCourseProgressGetterUseCase):

    def __init__(
        self,
        progress_repo: IProgressRepo,
        lesson_repo: ILessonRepo,
    ):
        self.__progress_repo = progress_repo
        self.__lesson_repo = lesson_repo

    async def get(self, course_id: UUID4, user_id: UUID4) -> tuple[Sequence[Progress], int]:
        progress = await self.__progress_repo.get_by_course(course_id, user_id)
        count = await self.__lesson_repo.count_by_course(course_id)

        return progress, count
