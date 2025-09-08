from catalog.domain.entities import Cart
from catalog.domain.exceptions import CartNotFoundError
from catalog.domain.services import CartService, ProductService
from catalog.domain.value_objects import Quantity

ProductIdInt = int
QuantityInt = int


class AddProductsToCartCommand:
    def __init__(
        self, cart_service: CartService, product_service: ProductService
    ):
        self._cart_service = cart_service
        self._product_service = product_service

    async def execute(
        self,
        user_id: int,
        products_ids_to_add_tuple: list[tuple[ProductIdInt, QuantityInt]],
    ) -> Cart:
        cart = await self._cart_service.get_cart(user_id=user_id)
        if cart is None:
            raise CartNotFoundError

        products = await self._product_service.get_by_ids(
            [product_id for product_id, _ in products_ids_to_add_tuple]
        )
        await self._cart_service.add_products(
            cart,
            [
                (product, Quantity(quantity))
                for product, (_, quantity) in zip(
                    products, products_ids_to_add_tuple, strict=False
                )
            ],
        )
        return cart
