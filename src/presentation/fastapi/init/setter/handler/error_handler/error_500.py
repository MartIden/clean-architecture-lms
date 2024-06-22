from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from src.presentation.fastapi.init.setter.handler.error_handler.abstract import AbstractErrorHandler


class Error500Handler(AbstractErrorHandler):
    @property
    def _http_code(self) -> int:
        return HTTP_500_INTERNAL_SERVER_ERROR
