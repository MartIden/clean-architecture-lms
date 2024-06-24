from dataclasses import dataclass, field
from typing import Generic, TypeVar, Optional

from pydantic import BaseModel

AnswerType = TypeVar("AnswerType")


def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )


class JsonSchema(BaseModel):
    class Config:
        frozen = True
        populate_by_name = True
        alias_generator = convert_field_to_camel_case


class AnswerError(JsonSchema):
    exception: str
    msg: str
    traceback: Optional[str] = None


class JsonResponse(Generic[AnswerType], JsonSchema):
    success: bool = True
    answer: AnswerType | None = None
    error: AnswerError | None = None
