from dependency_injector.wiring import Provide
from fastapi import Depends
from pydantic import UUID4

from src.domain.common.data_models import JsonResponse
from src.domain.course.dto.course import CourseInResponse
from src.domain.course.port.course_repo import ICourseRepo
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class ReadCourseController(IController[UUID4, JsonResponse[CourseInResponse]]):

    def __init__(
        self,
        course_repo: ICourseRepo = Depends(Provide[AppContainer.infrastructure.course_repo])
    ):
        self.__course_repo = course_repo

    async def __call__(self, id_: UUID4) -> JsonResponse[CourseInResponse]:
        course = await self.__course_repo.read_one(id_)
        return JsonResponse[CourseInResponse](answer=CourseInResponse.from_entity(course))
