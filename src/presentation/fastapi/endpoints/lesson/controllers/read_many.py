from dependency_injector.wiring import Provide
from fastapi import Depends

from src.domain.common.data_models import JsonResponse
from src.domain.lesson.dto.lesson import LessonManyInRequest, LessonsInResponse, LessonInResponse
from src.domain.lesson.port.lesson_repo import ILessonRepo
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class ReadManyLessonController(IController[LessonManyInRequest, JsonResponse[LessonsInResponse]]):

    def __init__(
        self,
        lesson_repo: ILessonRepo = Depends(Provide[AppContainer.infrastructure.lesson_repo])
    ):
        self.__lesson_repo = lesson_repo

    async def __call__(self, request: LessonManyInRequest) -> JsonResponse[LessonsInResponse]:
        lessons = await self.__lesson_repo.read_many(request.limit, request.offset, request.order, "created_at")
        count = await self.__lesson_repo.count()

        return JsonResponse[LessonsInResponse](
            answer=LessonsInResponse(
                rows=[LessonInResponse.from_lesson(lesson) for lesson in lessons],
                count=count
            )
        )
