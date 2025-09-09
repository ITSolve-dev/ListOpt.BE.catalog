from catalog.domain.entities import Cart
from catalog.domain.exceptions import CartNotFoundError
from catalog.domain.services import CartService


class ChangeQuantitiesProductsInCartCommand:
    def __init__(self, cart_service: CartService) -> None:
        self._cart_service = cart_service

    async def execute(
        self,
        user_id: int,
        products_and_quantities: list[tuple[int, int]],
    ) -> Cart:
        cart = await self._cart_service.get_cart(user_id=user_id)
        if cart is None:
            raise CartNotFoundError
        data: dict[int, int] = {}
        for product_id, quantity in products_and_quantities:
            data.update({product_id: quantity})
        await self._cart_service.change_quantities(cart, data)
        return cart
