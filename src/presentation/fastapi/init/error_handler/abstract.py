import traceback
from logging import Logger

from dependency_injector.wiring import Provide
from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette_context import context

from src.infrastructure.ioc.container.application import ApplicationContainer
from src.infrastructure.settings.stage.app import AppSettings


class AbstractErrorHandler:

    def __init__(
        self,
        app_settings: AppSettings = Provide[ApplicationContainer.core.settings],
        logger: Logger = Provide[ApplicationContainer.core.logger],
    ):
        self.__logger = logger
        self.__app_settings = app_settings

    def _base_handle_logic(self, exc: HTTPException) -> JSONResponse:
        error = {
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        }

        if self.__app_settings.SHOW_TRACEBACK_IN_RESPONSE:
            error["traceback"] = traceback.format_tb(exc.__traceback__)

        extra = {
            "success": False,
            "answer": None,
            "error": error,
        }

        json_response = JSONResponse(status_code=self._http_code, content=extra)

        extra["error"]["traceback"] = traceback.format_tb(exc.__traceback__)
        extra.update(context.data)

        self.__logger.error(msg=type(exc).__name__, extra=extra)

        return json_response

    async def handle(self, _: Request, exc: HTTPException) -> JSONResponse:
        return self._base_handle_logic(exc)
