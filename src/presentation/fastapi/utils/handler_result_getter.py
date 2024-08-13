from src.application.use_case.interface import IHandler
from src.domain.common.data_models import JsonResponse
from src.domain.common.dto.event import HandlerResult


class ResultsHttpGetter:

    def __init__(self, results: dict[type, HandlerResult]):
        self.__results = results

    def get(self, handler_type: type[IHandler], handler: callable) -> JsonResponse:
        result = self.__results.get(handler_type)

        if result and result.error:
            return JsonResponse(error=result.error)

        return JsonResponse(answer=handler(result.value))
