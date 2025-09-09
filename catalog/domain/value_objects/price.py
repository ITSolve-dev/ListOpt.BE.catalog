from decimal import Decimal
from typing import Annotated

from pydantic import Field
from pydantic.dataclasses import dataclass

from .value_object import ValueObject

PriceField = Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]


@dataclass(frozen=True, slots=True)
class Price(ValueObject):
    internal: PriceField
    external: PriceField
