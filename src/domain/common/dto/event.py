from uuid import uuid4

from pydantic import UUID4, Field

from src.domain.common.data_models import JsonModel


class Event(JsonModel):
    id: UUID4 = Field(default_factory=uuid4, frozen=True)
