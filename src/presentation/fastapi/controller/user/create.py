from pydantic import BaseModel

from src.presentation.fastapi.controller.interface import IController


class CreateUserRequest(BaseModel):
    login: str
    password: str


class UserInResponse(BaseModel):
    login: str


class CreateUserController(IController[CreateUserRequest, UserInResponse]):
    async def __call__(self, request: CreateUserRequest) -> UserInResponse:
        pass
