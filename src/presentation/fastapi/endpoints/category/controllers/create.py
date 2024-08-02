from dependency_injector.wiring import Provide
from fastapi import Depends

from src.domain.common.data_models import JsonResponse
from src.domain.category.dto.category import CategoryInCreate, CategoryInResponse
from src.domain.category.port.category_repo import ICategoryRepo
from src.infrastructure.ioc.container.application import AppContainer
from src.presentation.fastapi.endpoints.controller_interface import IController


class CreateCategoryController(IController[CategoryInCreate, JsonResponse[CategoryInResponse]]):

    def __init__(
        self,
        category_repo: ICategoryRepo = Depends(Provide[AppContainer.infrastructure.category_repo])
    ):
        self.__category_repo = category_repo

    async def __call__(self, request: CategoryInCreate) -> JsonResponse[CategoryInResponse]:
        category = await self.__category_repo.create(request)
        return JsonResponse[CategoryInResponse](answer=CategoryInResponse.from_entity(category))

