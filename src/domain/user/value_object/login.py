from dataclasses import dataclass

from src.domain.common.value_object import ValueObject


@dataclass
class UserLogin(ValueObject[str]):
    value: str
