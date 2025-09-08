from catalog.domain.entities import Cart
from catalog.domain.exceptions import CartNotFoundError
from catalog.domain.services import CartService


class RemoveProductsFromCartCommand:
    def __init__(self, cart_service: CartService):
        self._cart_service = cart_service

    async def execute(
        self,
        user_id: int,
        products_ids: list[int],
    ) -> Cart:
        cart = await self._cart_service.get_cart(user_id=user_id)
        if cart is None:
            raise CartNotFoundError

        await self._cart_service.remove_products(cart, products_ids)
        return cart
