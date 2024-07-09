from dependency_injector.wiring import Provide
from fastapi import Depends

from src.domain.common.data_models import JsonResponse, ManyJsonAnswer, ManyInRequest
from src.domain.lesson.dto.lesson import LessonInResponse
from src.domain.lesson.port.lesson_repo import ILessonRepo
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class ReadManyLessonController(IController[ManyInRequest, JsonResponse[ManyJsonAnswer[LessonInResponse]]]):

    def __init__(
        self,
        lesson_repo: ILessonRepo = Depends(Provide[AppContainer.infrastructure.lesson_repo])
    ):
        self.__lesson_repo = lesson_repo

    async def __call__(self, request: ManyInRequest) -> JsonResponse[ManyJsonAnswer[LessonInResponse]]:
        lessons = await self.__lesson_repo.read_many(request.limit, request.offset, request.order, "created_at")
        count = await self.__lesson_repo.count()

        return JsonResponse[ManyJsonAnswer[LessonInResponse]](
            answer=ManyJsonAnswer[LessonInResponse](
                rows=[LessonInResponse.from_lesson(lesson) for lesson in lessons],
                count=count
            )
        )
