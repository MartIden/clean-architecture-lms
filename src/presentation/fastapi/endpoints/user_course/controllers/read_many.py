from dependency_injector.wiring import Provide
from fastapi import Depends
from pydantic import UUID4

from src.domain.common.data_models import JsonResponse
from src.domain.course.dto.user_course import UserCourseManyInRequest, UserCoursesInResponse, UserCourseInResponse
from src.domain.course.port.user_course_repo import IUserCourseRepo
from src.domain.user.dto.user import UserInCreate, UserInResponse
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class ReadManyUserCourseController(IController[UserCourseManyInRequest, JsonResponse[UserCoursesInResponse]]):

    def __init__(
        self,
        user_course_repo: IUserCourseRepo = Depends(Provide[AppContainer.infrastructure.user_course_repo])
    ):
        self.__user_course_repo = user_course_repo

    async def __call__(self, request: UserCourseManyInRequest) -> JsonResponse[UserCoursesInResponse]:
        user_courses = await self.__user_course_repo.read_many(request.limit, request.offset, request.order, "created_at")
        count = await self.__user_course_repo.count()

        return JsonResponse[UserCoursesInResponse](
            answer=UserCoursesInResponse(
                rows=[UserCourseInResponse.from_entity(user_course) for user_course in user_courses],
                count=count
            )
        )
