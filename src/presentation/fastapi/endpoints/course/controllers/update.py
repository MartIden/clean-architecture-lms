from dependency_injector.wiring import Provide
from fastapi import Depends

from src.application.use_case.course.updater import ICourseUpdaterCase
from src.domain.common.data_models import JsonResponse
from src.domain.course.dto.course import (
    CourseInResponse,
    CourseInUpdateForUpdater
)
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class UpdateCourseController(IController[CourseInUpdateForUpdater, JsonResponse[CourseInResponse]]):

    def __init__(
        self,
        course_updater: ICourseUpdaterCase = Depends(Provide[AppContainer.services.course_updater_case])
    ):
        self.__course_updater = course_updater

    async def __call__(self, request: CourseInUpdateForUpdater) -> JsonResponse[CourseInResponse]:
        course = await self.__course_updater.update(request)
        return JsonResponse[CourseInResponse](answer=CourseInResponse.from_entity(course))


class UpdateCourseFullController(
    IController[
        CourseInUpdateForUpdater,
        JsonResponse[CourseInResponse]
    ]
):

    def __init__(
        self,
        course_updater: ICourseUpdaterCase = Depends(Provide[AppContainer.services.course_updater_case])
    ):
        self.__course_updater = course_updater

    async def __call__(self, request: CourseInUpdateForUpdater) -> JsonResponse[CourseInResponse]:
        course = await self.__course_updater.update(request)
        return JsonResponse[CourseInResponse](answer=CourseInResponse.from_entity(course))
