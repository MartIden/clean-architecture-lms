from dependency_injector.wiring import Provide
from fastapi import Depends

from src.domain.common.data_models import JsonResponse
from src.domain.course.dto.user_course import UserCourseInUpdate, UserCourseInResponse
from src.domain.course.port.user_course_repo import IUserCourseRepo
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class UpdateUserCourseController(IController[UserCourseInUpdate, JsonResponse[UserCourseInResponse]]):

    def __init__(
        self,
        user_course_repo: IUserCourseRepo = Depends(Provide[AppContainer.infrastructure.user_course_repo])
    ):
        self.__user_course_repo = user_course_repo

    async def __call__(self, request: UserCourseInUpdate) -> JsonResponse[UserCourseInResponse]:
        user_course = await self.__user_course_repo.update(request)
        return JsonResponse[UserCourseInResponse](answer=UserCourseInResponse.from_entity(user_course))
