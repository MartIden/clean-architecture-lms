from fastapi import APIRouter

from src.presentation.fastapi.endpoints.auth.router import auth_api
from src.presentation.fastapi.endpoints.course.router import course_api
from src.presentation.fastapi.endpoints.lesson.router import lesson_api
from src.presentation.fastapi.endpoints.progress.router import progres_api
from src.presentation.fastapi.endpoints.user.router import user_api
from src.presentation.fastapi.endpoints.user_course.router import user_course_api

""" API ROUTER """
api_router = APIRouter(prefix="/api/v1", tags=["API V1"])
api_router.include_router(auth_api)
api_router.include_router(user_api)
api_router.include_router(course_api)
api_router.include_router(lesson_api)
api_router.include_router(user_course_api)
api_router.include_router(progres_api)
