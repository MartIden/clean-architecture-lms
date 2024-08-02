from src.presentation.fastapi.endpoints.controller_interface import IController


class CreateController[RequestT, ResponseT](IController):

    _ANSWER_T = None

    def __init__(self, repo: object,):
        self.__repo = repo

    async def __call__(self, request: RequestT) -> ResponseT:
        course = await self.__repo.create(request)
        return self.__response_t(answer=self.__answer_t.from_entity(course))
