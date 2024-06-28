import json
import traceback

from fastapi import HTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
from starlette_context import context

from src.presentation.fastapi.init.setter.handler.error_handler.abstract import AbstractErrorHandler


class Error400Handler(AbstractErrorHandler):

    @property
    def _http_code(self) -> int:
        return HTTP_400_BAD_REQUEST

    def _base_handle_logic(self, exc: HTTPException) -> JSONResponse:

        fields = ", ".join([item.get("loc")[1] for item in exc.args[0]])

        error = {
            "errorType": type(exc).__name__,
            "msg": f"Field required: {fields}",
        }

        if self._app_settings.SHOW_TRACEBACK_IN_RESPONSE:
            error["traceback"] = traceback.format_tb(exc.__traceback__)

        extra = {
            "success": False,
            "answer": None,
            "error": error,
        }

        json_response = JSONResponse(status_code=self._http_code, content=extra)

        extra["error"]["traceback"] = str(traceback.format_tb(exc.__traceback__))
        extra.update(context.data)

        self._logger.error(msg=type(exc).__name__, extra=extra)

        return json_response
