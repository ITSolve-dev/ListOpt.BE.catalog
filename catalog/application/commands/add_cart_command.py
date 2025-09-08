from catalog.domain.entities import Cart
from catalog.domain.services.cart_service import CartService


class AddCartCommand:
    def __init__(self, cart_service: CartService):
        self.cart_service = cart_service

    async def execute(self, user_id: int) -> Cart:
        return await self.cart_service.create_cart(user_id)
