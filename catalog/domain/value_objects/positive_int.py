from typing import Any, Self

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class PositiveInt(int):
    def __new__(cls, value: int) -> Self:
        if value < 0:
            raise ValueError(f"{cls.__name__} must be greater than 0")
        return super().__new__(cls, value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(int))
