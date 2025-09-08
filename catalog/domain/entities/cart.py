from typing import cast

from pydantic import Field
from pydantic.dataclasses import dataclass

from catalog.domain.entities.product import Product
from catalog.domain.exceptions import (
    CartAlreadyHaveProductsError,
    CartNotFoundProductsError,
)
from catalog.domain.value_objects import Quantity, UserID

from .entity import Entity
from .product_in_cart import ProductInCart


@dataclass(kw_only=True)
class Cart(Entity):
    user_id: UserID = Field(gt=0)
    products: list[ProductInCart] = Field(default_factory=list)

    def change_quantities(
        self, products_and_quantities: dict[int, int]
    ) -> None:
        product_ids = products_and_quantities.keys()
        for product_in_cart in self.products:
            if not product_in_cart.product.id:
                raise RuntimeError(
                    f"Product in cart ID is None - {product_in_cart.product}"
                )
            if product_in_cart.product.id in product_ids:
                product_in_cart.quantity = Quantity(
                    products_and_quantities[product_in_cart.product.id]
                )

    def add_products(self, products: list[ProductInCart]) -> None:
        diff = set(products) - set(self.products)
        if len(diff) != len(set(products)):
            raise CartAlreadyHaveProductsError(
                ctx=dict(ids=[product.id for product in diff])
            )
        self.products.extend(products)

    def remove_products(self, products: list[Product]) -> None:
        cart_products = set([product.product for product in self.products])
        diff = set(products) - set(cart_products)
        if diff != set():
            raise CartNotFoundProductsError(
                ctx=dict(ids=[product.id for product in diff]),
                description="No such products for remove in cart",
            )
        self.products = [
            product
            for product in self.products
            if product.product not in products
        ]

    @property
    def total_price(self) -> float:
        return sum(
            float(product.product.price.internal) for product in self.products
        )

    @property
    def total_quantity(self) -> int:
        return sum(product.quantity for product in self.products)

    def __len__(self) -> int:
        return len(self.products)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cart):
            raise TypeError("Cannot compare Cart with non-Cart object")
        if self.user_id != other.user_id:
            return False
        return super().__eq__(other)

    def __hash__(self) -> int:
        return hash(self.user_id)
