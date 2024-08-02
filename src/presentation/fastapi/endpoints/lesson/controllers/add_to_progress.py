from dependency_injector.wiring import Provide
from fastapi import Depends
from pydantic import UUID4

from src import AppContainer
from src.domain.user.dto.user import UserSlim
from src.domain.user.enum.roles import ALL_ROLES
from src.domain.common.data_models import JsonResponse
from src.presentation.fastapi.depends.auth import has_roles
from src.domain.progress.dto.progress import ProgressInResponse
from src.application.use_case.progress.adder import IProgressAdderCase
from src.presentation.fastapi.endpoints.controller_interface import IController


class AddToProgressController(IController[UUID4, JsonResponse[ProgressInResponse]]):

    def __init__(
        self,
        user: UserSlim = Depends(has_roles(ALL_ROLES)),
        course_adder_case: IProgressAdderCase = Depends(Provide[AppContainer.services.progress_adder_case])
    ):
        self.__user = user
        self.__course_adder_case = course_adder_case

    async def __call__(self, request: UUID4) -> JsonResponse[ProgressInResponse]:
        progress = await self.__course_adder_case.add(lesson_id=request, user=self.__user)
        progress_in_response = ProgressInResponse.from_entity(progress)
        return JsonResponse[ProgressInResponse](answer=progress_in_response)
