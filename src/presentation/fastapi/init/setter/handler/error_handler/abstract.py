import traceback
from abc import ABC
from logging import Logger

from dependency_injector.wiring import inject
from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette_context import context

from src.infrastructure.settings.stage.app import AppSettings
from src.presentation.fastapi.init.setter.handler.error_handler.interface import IErrorHandler


class AbstractErrorHandler(IErrorHandler, ABC):

    @inject
    def __init__(
        self,
        app_settings: AppSettings,
        logger: Logger,
    ):
        self.__logger = logger
        self.__app_settings = app_settings

    def _base_handle_logic(self, exc: HTTPException) -> JSONResponse:
        error = {
            "errorType": type(exc).__name__,
            "msg": str(exc),
        }

        if self.__app_settings.SHOW_TRACEBACK_IN_RESPONSE:
            error["traceback"] = str(traceback.format_tb(exc.__traceback__))

        extra = {
            "success": False,
            "answer": None,
            "error": error,
        }

        json_response = JSONResponse(status_code=self._http_code, content=extra)

        extra["error"]["traceback"] = str(traceback.format_tb(exc.__traceback__))
        extra.update(context.data)

        self.__logger.error(msg=type(exc).__name__, extra=extra)

        return json_response

    async def handle(self, _: Request, exc: HTTPException) -> JSONResponse:
        return self._base_handle_logic(exc)
