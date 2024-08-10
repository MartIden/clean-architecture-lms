from dependency_injector.wiring import Provide
from fastapi import Depends
from pydantic import UUID4

from src.domain.common.data_models import (
    JsonResponse,
    ManyJsonAnswer
)
from src.domain.user.dto.user import UserSlim
from src.domain.user.enum.roles import ALL_ROLES
from src.presentation.fastapi.depends.auth import has_roles
from src.domain.progress.dto.progress import ProgressInResponse
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController
from src.application.handler.progress.by_course_getter import IByCourseProgressGetterUseCase


class ReadProgressByCourseController(IController[UUID4, JsonResponse[ManyJsonAnswer[ProgressInResponse]]]):

    def __init__(
        self,
        user: UserSlim = Depends(has_roles(ALL_ROLES)),
        by_course_progress_getter_case: IByCourseProgressGetterUseCase = Depends(
            Provide[AppContainer.services.by_course_progress_getter_case]
        )
    ):
        self.__user = user
        self.__by_course_progress_getter_case = by_course_progress_getter_case

    async def __call__(self, id_: UUID4) -> JsonResponse[ManyJsonAnswer[ProgressInResponse]]:
        progresses, count = await self.__by_course_progress_getter_case.get(id_, self.__user.id)
        return JsonResponse[ManyJsonAnswer[ProgressInResponse]](
            answer=ManyJsonAnswer[ProgressInResponse](
                rows=[ProgressInResponse.from_entity(progress) for progress in progresses if progress],
                count=count
            )
        )
