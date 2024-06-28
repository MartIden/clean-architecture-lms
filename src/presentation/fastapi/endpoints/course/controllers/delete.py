from dependency_injector.wiring import Provide
from fastapi import Depends
from pydantic import UUID4

from src.domain.common.data_models import JsonResponse
from src.domain.course.dto.course import CourseInCreate, CourseInResponse
from src.domain.course.port.course_repo import ICourseRepo
from src.domain.user.dto.user import UserInCreate, UserInResponse
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class DeleteCourseController(IController[UserInCreate, JsonResponse[UserInResponse]]):

    def __init__(
        self,
        course_repo: ICourseRepo = Depends(Provide[AppContainer.infrastructure.course_repo])
    ):
        self.__course_repo = course_repo

    async def __call__(self, id_: UUID4) -> JsonResponse[CourseInResponse]:
        course = await self.__course_repo.delete(id_)
        return JsonResponse[CourseInResponse](answer=CourseInResponse.from_course(course))
