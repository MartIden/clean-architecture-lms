from dependency_injector.wiring import Provide
from fastapi import Depends
from pydantic import UUID4

from src.domain.common.data_models import JsonResponse
from src.domain.course.dto.course import CourseInCreate, CourseInResponse, CourseManyInRequest, CoursesInResponse
from src.domain.course.port.course_repo import ICourseRepo
from src.domain.user.dto.user import UserInCreate, UserInResponse
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class ReadManyCourseController(IController[UserInCreate, JsonResponse[UserInResponse]]):

    def __init__(
        self,
        course_repo: ICourseRepo = Depends(Provide[AppContainer.infrastructure.course_repo])
    ):
        self.__course_repo = course_repo

    async def __call__(self, request: CourseManyInRequest) -> JsonResponse[CoursesInResponse]:
        courses = await self.__course_repo.read_many(request.limit, request.offset, request.order, "created_at")
        count = await self.__course_repo.count()

        return JsonResponse[CoursesInResponse](
            answer=CoursesInResponse(
                rows=[CourseInResponse.from_course(course) for course in courses],
                count=count
            )
        )
