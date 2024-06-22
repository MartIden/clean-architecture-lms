from starlette_context.middleware import RawContextMiddleware
from starlette_context import plugins

from src.presentation.fastapi.init.setter.handler.middleware.interface import IMiddlewareHandler


class RawContexMiddlewareHandler(IMiddlewareHandler):

    @property
    def middleware_class(self) -> type:
        return RawContextMiddleware

    @property
    def kwargs(self) -> dict:
        return {
            "plugins": (
                plugins.RequestIdPlugin(),
                plugins.CorrelationIdPlugin(),
                plugins.ForwardedForPlugin(),
                plugins.UserAgentPlugin()
            ),
        }
