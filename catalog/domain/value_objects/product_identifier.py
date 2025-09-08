from pydantic import Field
from pydantic.dataclasses import dataclass

from .value_object import ValueObject


@dataclass(frozen=True, slots=True)
class ProductIdentifier(ValueObject):
    # TODO: Add validation for article and barcode
    article: str = Field()
    barcode: str = Field()

    def __hash__(self) -> int:
        return hash(self.article + self.barcode)
