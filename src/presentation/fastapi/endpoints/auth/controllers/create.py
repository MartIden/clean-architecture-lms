from dependency_injector.wiring import Provide
from fastapi import Depends

from src.domain.common.data_models import JsonResponse
from src.domain.user.dto.user import UserInResponse, UserInCreateEvent
from src.infrastructure.ioc.container.application import AppContainer
from src.infrastructure.mediator.interface import IMediator
from src.presentation.fastapi.endpoints.controller_interface import IController


class CreateUserController(IController[UserInCreateEvent, JsonResponse[UserInResponse]]):

    def __init__(self, mediator: IMediator = Depends(Provide[AppContainer.handlers.mediator])):
        self.__mediator = mediator

    async def __call__(self, request: UserInCreateEvent) -> JsonResponse[UserInResponse]:
        user = await self.__mediator.dispatch(request)
        return JsonResponse[UserInResponse](answer=UserInResponse.from_entity(user))
