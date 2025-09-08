from typing import Self

from .non_empty_str import NonEmptyStr


class ProductName(NonEmptyStr):
    def __new__(cls, value: str) -> Self:
        if len(value) < 2 or len(value) > 100:
            raise ValueError("Product name must be between 2 and 100 characters")
        return super().__new__(cls, value)
