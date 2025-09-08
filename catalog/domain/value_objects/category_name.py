from typing import Self

from .non_empty_str import NonEmptyStr


class CategoryName(NonEmptyStr):
    MIN_LENGTH = 1
    MAX_LENGTH = 100
    VALIDATION_ERROR_MESSAGE = f"Category name must be between {MIN_LENGTH} and {MAX_LENGTH} characters"  # noqa: E501

    def __new__(cls, value: str) -> Self:
        if len(value) < cls.MIN_LENGTH or len(value) > cls.MAX_LENGTH:
            raise ValueError(cls.VALIDATION_ERROR_MESSAGE)
        return super().__new__(cls, value)
