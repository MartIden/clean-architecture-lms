from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from starlette.requests import Request

from src.infrastructure.ioc.container.application import AppContainer
from src.infrastructure.settings.stage.app import AppSettings

docs_api = APIRouter(prefix="/docs", tags=["docs"])


@docs_api.get("/", include_in_schema=False)
async def get_swagger_documentation():
    return get_swagger_ui_html(openapi_url="/docs/openapi.json", title="docs")


@docs_api.get("/redoc", include_in_schema=False)
async def get_redoc_documentation():
    return get_redoc_html(openapi_url="/docs/openapi.json", title="docs")


@docs_api.get("/openapi.json", include_in_schema=False)
@inject
async def openapi(
    request: Request,
    settings: AppSettings = Depends(Provide[AppContainer.core.settings]),
):
    return get_openapi(title=settings.TITLE, version=settings.VERSION, routes=request.app.routes)
