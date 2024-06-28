from dependency_injector.wiring import Provide
from fastapi import Depends
from pydantic import UUID4

from src.domain.common.data_models import JsonResponse
from src.domain.lesson.dto.lesson import LessonInResponse
from src.domain.lesson.port.lesson_repo import ILessonRepo
from src.domain.user.dto.user import UserInCreate, UserInResponse
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class DeleteLessonController(IController[UserInCreate, JsonResponse[UserInResponse]]):

    def __init__(
        self,
        lesson_repo: ILessonRepo = Depends(Provide[AppContainer.infrastructure.lesson_repo])
    ):
        self.__lesson_repo = lesson_repo

    async def __call__(self, id_: UUID4) -> JsonResponse[LessonInResponse]:
        lesson = await self.__lesson_repo.delete(id_)
        return JsonResponse[LessonInResponse](answer=LessonInResponse.from_lesson(lesson))
