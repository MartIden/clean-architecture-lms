from typing import TypeVar, Generic

from pydantic import BaseModel

from src.domain.common.enum.order import Order
from src.domain.common.value_obj.limit import Limit


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


RowT = TypeVar("RowT", bound=JsonModel)


class ManyJsonAnswer(JsonModel, Generic[RowT]):
    rows: list[RowT] | None
    count: int


class ManyInRequest(JsonModel):
    limit: Limit
    offset: int
    order: Order


class ErrorAnswer(JsonModel):
    error_type: str
    msg: str
    traceback: str | list[str] | None = None


AnswerT = TypeVar("AnswerT", bound=JsonModel)


class JsonResponse(JsonModel, Generic[AnswerT]):
    success: bool = True
    answer: AnswerT | None = None
    error: ErrorAnswer | None = None
