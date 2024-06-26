from fastapi import APIRouter

from src.presentation.fastapi.endpoints.user.router import user_api

""" API ROUTER """
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(user_api)


admin_router = APIRouter(prefix="/api/v1/admin")
