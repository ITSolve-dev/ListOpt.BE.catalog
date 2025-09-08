from pydantic import Field
from pydantic.dataclasses import dataclass

from ..value_objects.quantity import Quantity
from .entity import Entity
from .product import Product


@dataclass(kw_only=True)
class ProductInCart(Entity):
    product: Product = Field()
    quantity: Quantity = Field(gt=0)
