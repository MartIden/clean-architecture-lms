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

    def __create_response_message(self, exc: HTTPException) -> dict:
        fields = [f"{item.get('msg')}: {item.get('loc')[1]}" for item in exc.args[0]]

        error = {
            "errorType": type(exc).__name__,
            "msg": fields,
        }

        if self._app_settings.SHOW_TRACEBACK_IN_RESPONSE:
            error["traceback"] = traceback.format_tb(exc.__traceback__)

        return {
            "success": False,
            "answer": None,
            "error": error,
        }


    def _base_handle_logic(self, exc: HTTPException) -> JSONResponse:

        msg = self.__create_response_message(exc)
        json_response = JSONResponse(status_code=self._http_code, content=msg)

        msg["error"]["traceback"] = str(traceback.format_tb(exc.__traceback__))
        msg.update(context.data)

        self._logger.error(msg=type(exc).__name__, extra=msg)
        return json_response
