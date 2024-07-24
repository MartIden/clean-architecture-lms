from dependency_injector.wiring import Provide
from fastapi import Depends

from src.domain.common.data_models import JsonResponse
from src.domain.course.dto.course import CourseInCreate, CourseInResponse
from src.domain.course.port.course_repo import ICourseRepo
from src.domain.user.enum.roles import UserRoleEnum
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.depends.auth import has_roles
from src.presentation.fastapi.endpoints.controller_interface import IController


class CreateCourseController(IController[CourseInCreate, JsonResponse[CourseInResponse]]):

    def __init__(
        self,
        course_repo: ICourseRepo = Depends(Provide[AppContainer.infrastructure.course_repo]),
    ):
        self.__course_repo = course_repo

    async def __call__(self, request: CourseInCreate) -> JsonResponse[CourseInResponse]:
        course = await self.__course_repo.create(request)
        return JsonResponse[CourseInResponse](answer=CourseInResponse.from_entity(course))
