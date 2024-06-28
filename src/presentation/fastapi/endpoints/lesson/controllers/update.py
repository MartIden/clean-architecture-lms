from dependency_injector.wiring import Provide
from fastapi import Depends

from src.domain.common.data_models import JsonResponse
from src.domain.lesson.dto.lesson import LessonInUpdate, LessonInResponse
from src.domain.lesson.port.lesson_repo import ILessonRepo
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class UpdateLessonController(IController[LessonInUpdate, JsonResponse[LessonInResponse]]):

    def __init__(
        self,
        lesson_repo: ILessonRepo = Depends(Provide[AppContainer.infrastructure.lesson_repo])
    ):
        self.__lesson_repo = lesson_repo

    async def __call__(self, request: LessonInUpdate) -> JsonResponse[LessonInResponse]:
        lesson = await self.__lesson_repo.update(request)
        return JsonResponse[LessonInResponse](answer=LessonInResponse.from_lesson(lesson))
