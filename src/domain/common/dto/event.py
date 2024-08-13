from typing import Optional, Any
from uuid import uuid4

from pydantic import UUID4, Field

from src.domain.common.data_models import JsonModel, ErrorAnswer


class Event(JsonModel):
    id: UUID4 = Field(default_factory=uuid4, frozen=True)


class HandlerResult(JsonModel):
    status: bool
    value: Any
    error: Optional[ErrorAnswer] = None
