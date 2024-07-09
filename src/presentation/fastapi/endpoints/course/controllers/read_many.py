from dependency_injector.wiring import Provide
from fastapi import Depends

from src.domain.common.data_models import JsonResponse, ManyJsonAnswer, ManyInRequest
from src.domain.course.dto.course import (
    CourseInResponse,
)
from src.domain.course.port.course_repo import ICourseRepo
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class ReadManyCourseController(IController[ManyInRequest, JsonResponse[ManyJsonAnswer[CourseInResponse]]]):

    def __init__(
        self,
        course_repo: ICourseRepo = Depends(Provide[AppContainer.infrastructure.course_repo])
    ):
        self.__course_repo = course_repo

    async def __call__(self, request: ManyInRequest) -> JsonResponse[ManyJsonAnswer[CourseInResponse]]:
        courses = await self.__course_repo.read_many(request.limit, request.offset, request.order, "created_at")
        count = await self.__course_repo.count()

        return JsonResponse[ManyJsonAnswer[CourseInResponse]](
            answer=ManyJsonAnswer[CourseInResponse](
                rows=[CourseInResponse.from_course(course) for course in courses],
                count=count
            )
        )
