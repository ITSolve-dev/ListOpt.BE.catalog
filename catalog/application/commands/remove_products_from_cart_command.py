from catalog.domain.entities import Cart
from catalog.domain.exceptions import CartNotFoundError
from catalog.domain.services import CartService, ProductService


class RemoveProductsFromCartCommand:
    def __init__(
        self, cart_service: CartService, product_service: ProductService
    ) -> None:
        self._cart_service = cart_service
        self._product_service = product_service

    async def execute(
        self,
        user_id: int,
        product_ids: list[int],
    ) -> Cart:
        cart = await self._cart_service.get_cart(user_id=user_id)
        if cart is None:
            raise CartNotFoundError
        products_to_remove = await self._product_service.get_by_ids(
            product_ids
        )
        await self._cart_service.remove_products(
            cart, list(products_to_remove)
        )
        return cart
