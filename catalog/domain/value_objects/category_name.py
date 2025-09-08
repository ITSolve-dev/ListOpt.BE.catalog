from typing import Self

from .non_empty_str import NonEmptyStr


class CategoryName(NonEmptyStr):
    def __new__(cls, value: str) -> Self:
        if len(value) < 1 or len(value) > 100:
            raise ValueError("Category name must be between 1 and 100 characters")
        return super().__new__(cls, value)
