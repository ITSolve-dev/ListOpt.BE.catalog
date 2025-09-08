from typing import cast

from pydantic import Field
from pydantic.dataclasses import dataclass

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

    def change_quantities(self, products_and_quantities: dict[int, int]) -> None:
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
        ids = [p.product.id for p in products]
        if None in ids:
            raise RuntimeError("None value in product ids to add to cart")
        ids = cast(list[int], ids)
        intersaction_ids = self.__get_intersection_product_ids(ids)
        if intersaction_ids:
            raise CartAlreadyHaveProductsError(ctx=dict(ids=intersaction_ids))
        self.products.extend(products)

    def remove_products(self, product_ids: list[int]) -> None:
        intersaction_ids = self.__get_intersection_product_ids(product_ids)
        if len(intersaction_ids) != len(product_ids):
            raise CartNotFoundProductsError(
                ctx=dict(ids=intersaction_ids),
                description="No such products for remove in cart",
            )
        self.products = [
            product
            for product in self.products
            if product.product.id not in product_ids
        ]

    @property
    def total_price(self) -> float:
        return sum(float(product.product.price.internal) for product in self.products)

    @property
    def total_quantity(self) -> int:
        return sum(product.quantity for product in self.products)

    def __get_intersection_product_ids(self, products: list[int]) -> list[int]:
        def only_product_id(product: ProductInCart):
            return product.product.id

        ids: list[int] = cast(
            list[int],
            list(set(map(only_product_id, self.products)).intersection(set(products))),
        )
        return ids

    def __len__(self):
        return len(self.products)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cart):
            raise ValueError("Cannot compare Cart with non-Cart object")
        if self.user_id != other.user_id:
            return False
        return super().__eq__(other)
