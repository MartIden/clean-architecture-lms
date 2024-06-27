from typing import Any, TypeVar

from pydantic import BaseModel


def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )


class JsonModel(BaseModel):
    class Config:
        frozen = True
        populate_by_name = True
        alias_generator = convert_field_to_camel_case


class ErrorAnswer(JsonModel):
    error_type: str
    msg: str
    traceback: str | list[str] | None = None


AnswerT = TypeVar("AnswerT", bound=JsonModel)


class JsonResponse[AnswerT](JsonModel):
    success: bool = True
    answer: AnswerT | None = None
    error: ErrorAnswer | None = None
