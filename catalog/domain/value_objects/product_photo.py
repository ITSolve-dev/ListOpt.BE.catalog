from typing import Self

from pydantic import HttpUrl

from .non_empty_str import NonEmptyStr


class ProductPhoto(NonEmptyStr):
    def __new__(cls, value: str) -> Self:
        try:
            HttpUrl(value)
        except ValueError:
            raise ValueError("Product photo must be a valid URL")
        return super().__new__(cls, value)
