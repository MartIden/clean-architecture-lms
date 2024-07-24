from dependency_injector.wiring import Provide
from fastapi import Depends
from pydantic import UUID4

from src.domain.common.data_models import JsonResponse
from src.domain.course.dto.user_course import UserCourseInResponse
from src.domain.course.port.user_course_repo import IUserCourseRepo
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class DeleteUserCourseController(IController[UUID4, JsonResponse[UserCourseInResponse]]):

    def __init__(
        self,
        user_course_repo: IUserCourseRepo = Depends(Provide[AppContainer.infrastructure.user_course_repo])
    ):
        self.__user_course_repo = user_course_repo

    async def __call__(self, id_: UUID4) -> JsonResponse[UserCourseInResponse]:
        course = await self.__user_course_repo.delete(id_)
        return JsonResponse[UserCourseInResponse](answer=UserCourseInResponse.from_entity(course))
