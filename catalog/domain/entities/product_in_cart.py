from pydantic import Field
from pydantic.dataclasses import dataclass

from catalog.domain.entities.entity import Entity
from catalog.domain.entities.product import Product
from catalog.domain.value_objects.quantity import Quantity


@dataclass(kw_only=True)
class ProductInCart(Entity):
    product: Product = Field()
    quantity: Quantity = Field(gt=0)

    def __hash__(self) -> int:
        return hash(self.quantity) + hash(self.product)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ProductInCart):
            return NotImplemented
        return (
            self.product == other.product and self.quantity == other.quantity
        )
