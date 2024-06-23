import json
from logging import Logger

from dependency_injector.wiring import Provide, inject
from fastapi import Request, Depends
from starlette_context import context

from src.infrastructure.ioc.container.application import AppContainer


class RequestJSONLoggerDepend:

    @classmethod
    async def __create_log_message(cls, request: Request) -> dict:
        unprepared_body = str(await request.body(), "utf-8")

        try:
            body = json.loads(unprepared_body)
        except json.decoder.JSONDecodeError:
            body = unprepared_body

        return {
            "url": request.url.path,
            "method": request.method,
            "queries": request.query_params,
            "body": body,
            **context.data,
        }

    @classmethod
    @inject
    async def log_it(cls, request: Request, logger: Logger = Depends(Provide[AppContainer.core.logger])) -> None:
        msg = await cls.__create_log_message(request)
        logger.info("request_data", extra=msg)
