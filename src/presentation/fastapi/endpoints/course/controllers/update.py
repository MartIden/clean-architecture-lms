from dependency_injector.wiring import Provide
from fastapi import Depends

from src.application.use_case.course.updater import CourseUpdaterCase, ICourseUpdaterCase
from src.domain.common.data_models import JsonResponse
from src.domain.course.dto.course import (
    CourseInResponse,
    CourseInUpdateEvent, CourseInUpdate
)
from src.infrastructure.ioc.container.application import AppContainer
from src.infrastructure.mediator.interface import IMediator
from src.presentation.fastapi.endpoints.controller_interface import IController
from src.presentation.fastapi.utils.handler_result_getter import ResultsHttpGetter


class UpdateCourseController(IController[CourseInUpdateEvent, JsonResponse[CourseInResponse]]):

    def __init__(
        self,
        course_updater_case: ICourseUpdaterCase = Depends(Provide[AppContainer.services.course_updater_case])
    ):
        self.__course_updater_case = course_updater_case

    async def __call__(self, request: CourseInUpdate) -> JsonResponse[CourseInResponse]:
        course = await self.__course_updater_case(request)
        return JsonResponse[CourseInResponse](answer=CourseInResponse.from_entity(course))


class UpdateCourseFullController(
    IController[
        CourseInUpdate,
        JsonResponse[CourseInResponse]
    ]
):

    def __init__(
        self,
        course_updater_case: ICourseUpdaterCase = Depends(Provide[AppContainer.services.course_updater_case])
    ):
        self.__course_updater_case = course_updater_case

    async def __call__(self, request: CourseInUpdate) -> JsonResponse[CourseInResponse]:
        course = await self.__course_updater_case(request)
        return JsonResponse[CourseInResponse](answer=CourseInResponse.from_entity(course))
