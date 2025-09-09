from pydantic import Field
from pydantic.dataclasses import dataclass

from catalog.domain.value_objects import PositiveInt

from .entity import Entity


@dataclass(kw_only=True)
class ProductField(Entity):
    name: str = Field()
    value: str = Field()
    measure: str = Field()
    product_id: PositiveInt = Field(init=False)
