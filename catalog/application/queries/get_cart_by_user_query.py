from catalog.domain.entities import Cart
from catalog.domain.services.cart_service import CartService


class GetCartByUserQuery:
    def __init__(self, cart_service: CartService):
        self.cart_service = cart_service

    async def __call__(self, user_id: int) -> Cart | None:
        return await self.cart_service.get_cart(user_id)
