from dependency_injector.wiring import Provide
from fastapi import Depends

from src.domain.common.data_models import JsonResponse, ManyJsonAnswer, ManyInRequest
from src.domain.category.dto.category import CategoryInResponse
from src.domain.category.port.category_repo import ICategoryRepo
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class ReadManyCategoryController(IController[ManyInRequest, JsonResponse[ManyJsonAnswer[CategoryInResponse]]]):

    def __init__(
        self,
        category_repo: ICategoryRepo = Depends(Provide[AppContainer.infrastructure.category_repo])
    ):
        self.__category_repo = category_repo

    async def __call__(self, request: ManyInRequest) -> JsonResponse[ManyJsonAnswer[CategoryInResponse]]:
        categorys = await self.__category_repo.read_many(request.limit, request.offset, request.order, "created_at")
        count = await self.__category_repo.count()

        return JsonResponse[ManyJsonAnswer[CategoryInResponse]](
            answer=ManyJsonAnswer[CategoryInResponse](
                rows=[CategoryInResponse.from_entity(category) for category in categorys],
                count=count
            )
        )

