from abc import abstractmethod, ABC
from typing import Any, Type

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from pydantic_core.core_schema import SimpleSerSchema


class DictVO(dict, ABC):

    @classmethod
    def __get_pydantic_core_schema__(
            cls, source: Type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls.__validator,
            core_schema.dict_schema(),
            serialization=SimpleSerSchema(type="dict"),
        )

    @classmethod
    def __validator(cls, v: dict, _info):
        cls._validate(v)
        return v

    @classmethod
    @abstractmethod
    def _validate(cls, value: dict) -> None:
        pass
