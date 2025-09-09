from catalog.domain.entities import Cart
from catalog.domain.entities.product import Product
from catalog.domain.entities.product_in_cart import ProductInCart
from catalog.domain.exceptions import (
    CartAlreadyExistsError,
    CartGetError,
    CartSaveError,
)
from catalog.domain.ports.uow import AbstractUnitOfWork
from catalog.domain.value_objects import UserID
from catalog.domain.value_objects.quantity import Quantity


class CartService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow = uow

    async def get_cart(self, user_id: int) -> Cart | None:
        async with self._uow:
            await self._uow.cart_repo.get(user_id)
            try:
                cart = await self._uow.cart_repo.get(user_id)
            except Exception as e:
                raise CartGetError(ctx={"user_id": user_id}) from e
        return cart

    async def create_cart(self, user_id: int) -> Cart:
        async with self._uow:
            is_exists = await self.get_cart(user_id)
            if is_exists:
                raise CartAlreadyExistsError(ctx={"user_id": user_id})
            cart = Cart(user_id=UserID(user_id))
            try:
                await self._uow.cart_repo.save(cart)
            except Exception as e:
                raise CartSaveError(ctx={"user_id": user_id}) from e
        return cart

    async def add_products(
        self, cart: Cart, products_to_add: list[tuple[Product, Quantity]]
    ) -> Cart:
        products = [
            ProductInCart(product=product, quantity=quantity)
            for product, quantity in products_to_add
        ]
        cart.add_products(products)
        async with self._uow:
            await self._uow.cart_repo.save(cart)
        return cart

    async def remove_products(
        self, cart: Cart, products: list[Product]
    ) -> Cart:
        cart.remove_products(products)
        async with self._uow:
            await self._uow.cart_repo.save(cart)
        return cart

    async def change_quantities(
        self, cart: Cart, data: dict[int, int]
    ) -> Cart:
        cart.change_quantities(data)
        async with self._uow:
            await self._uow.cart_repo.save(cart)
        return cart
