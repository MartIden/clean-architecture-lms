from abc import abstractmethod, ABC
from typing import Any, Type

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from pydantic_core.core_schema import SimpleSerSchema


class IntVO(int, ABC):

    @classmethod
    def __get_pydantic_core_schema__(
            cls, source: Type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls.__validator,
            core_schema.int_schema(),
            serialization=SimpleSerSchema(type="int"),
        )

    @classmethod
    def __validator(cls, v: int, _info) -> int:
        cls._validate(v)
        return v

    @classmethod
    @abstractmethod
    def _validate(cls, value: int) -> None:
        pass


class PositiveInt(IntVO):

    @classmethod
    def _validate(cls, value: int) -> None:
        if value < 0:
            raise ValueError("Value Must Be > 0")
