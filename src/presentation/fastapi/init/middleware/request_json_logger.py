import json
from logging import Logger

from dependency_injector.wiring import Provide
from fastapi import Request
from starlette_context import context

from src.infrastructure.ioc.container.application import AppContainer


class RequestJSONLoggerMiddleware:
    def __init__(self, request: Request, logger: Logger):
        self.__logger = logger
        self.__request: Request = request

    @property
    async def log_message(self) -> dict:
        unprepared_body = str(await self.__request.body(), "utf-8")

        try:
            body = json.loads(unprepared_body)
        except json.decoder.JSONDecodeError:
            body = unprepared_body

        return {
            "url": self.__request.url.path,
            "method": self.__request.method,
            "queries": self.__request.query_params,
            "body": body,
            **context.data,
        }

    async def log(self):
        log = await self.log_message
        self.__logger.info("request_data", extra=log)

    @staticmethod
    async def log_middle(request: Request, logger: Logger = Provide[AppContainer.core.logger]):
        try:
            logging_middleware = RequestJSONLoggerMiddleware(request, logger)
            await logging_middleware.log()
        except Exception:
            pass
