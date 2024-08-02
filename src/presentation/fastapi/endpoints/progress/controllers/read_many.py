from dependency_injector.wiring import Provide
from fastapi import Depends
from pydantic import UUID4

from src.domain.common.data_models import JsonResponse, ManyInRequest, ManyJsonAnswer
from src.domain.progress.dto.progress import ProgressInResponse, ProgressInCreate
from src.domain.progress.ports.progress_repo import IProgressRepo
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class ReadManyProgressController(IController[UUID4, JsonResponse[ProgressInResponse]]):

    def __init__(
        self,
        progress_repo: IProgressRepo = Depends(Provide[AppContainer.infrastructure.progress_repo])
    ):
        self.__progress_repo = progress_repo

    async def __call__(self, request: ManyInRequest) -> JsonResponse[ManyJsonAnswer[ProgressInResponse]]:
        progress_many = await self.__progress_repo.read_many(
            request.limit, request.offset, request.order, "created_at"
        )
        count = await self.__progress_repo.count()

        return JsonResponse[ManyJsonAnswer[ProgressInResponse]](
            answer=ManyJsonAnswer[ProgressInResponse](
                rows=[ProgressInResponse.from_entity(progress) for progress in progress_many],
                count=count
            )
        )
