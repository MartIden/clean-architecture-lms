from dependency_injector.wiring import Provide
from fastapi import Depends

from src.domain.common.data_models import JsonResponse
from src.domain.progress.dto.progress import ProgressInResponse, ProgressInCreate
from src.domain.progress.ports.progress_repo import IProgressRepo
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class CreateProgressController(IController[ProgressInCreate, JsonResponse[ProgressInResponse]]):

    def __init__(
        self,
        progress_repo: IProgressRepo = Depends(Provide[AppContainer.infrastructure.progress_repo])
    ):
        self.__progress_repo = progress_repo

    async def __call__(self, request: ProgressInCreate) -> JsonResponse:
        lesson = await self.__progress_repo.create(request)
        return JsonResponse(answer=ProgressInResponse.from_entity(lesson))
