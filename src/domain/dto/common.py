from dataclasses import dataclass, field
from typing import Generic, TypeVar, Optional

AnswerType = TypeVar("AnswerType")


@dataclass(slots=True, frozen=True)
class AnswerError:
    exception: str
    msg: str
    traceback: Optional[str] = None


@dataclass(slots=True, frozen=True)
class JsonResponse(Generic[AnswerType]):
    success: bool = True
    answer: Optional[AnswerType] = None
    error: Optional[AnswerError] = None

