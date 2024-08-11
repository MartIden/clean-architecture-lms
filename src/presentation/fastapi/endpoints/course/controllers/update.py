from dependency_injector.wiring import Provide
from fastapi import Depends

from src.domain.common.data_models import JsonResponse
from src.domain.course.dto.course import (
    CourseInResponse,
    CourseInUpdateEvent
)
from src.infrastructure.ioc.container.application import AppContainer
from src.infrastructure.mediator.interface import IMediator
from src.presentation.fastapi.endpoints.controller_interface import IController


class UpdateCourseController(IController[CourseInUpdateEvent, JsonResponse[CourseInResponse]]):

    def __init__(self, mediator: IMediator = Depends(Provide[AppContainer.handlers.mediator])):
        self.__mediator = mediator

    async def __call__(self, request: CourseInUpdateEvent) -> JsonResponse[CourseInResponse]:
        course = await self.__mediator.dispatch(request)
        return JsonResponse[CourseInResponse](answer=CourseInResponse.from_entity(course))


class UpdateCourseFullController(
    IController[
        CourseInUpdateEvent,
        JsonResponse[CourseInResponse]
    ]
):

    def __init__(
        self,
        mediator: IMediator = Depends(Provide[AppContainer.handlers.mediator])
    ):
        self.__mediator = mediator

    async def __call__(self, request: CourseInUpdateEvent) -> JsonResponse[CourseInResponse]:
        course = await self.__mediator.dispatch(request)
        return JsonResponse[CourseInResponse](answer=CourseInResponse.from_entity(course))
