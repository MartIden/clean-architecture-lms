from dataclasses import dataclass
from typing import TypeVar, Generic

ValueT = TypeVar("ValueT")


@dataclass
class ValueObject(Generic[ValueT]):
    value: ValueT
