from decimal import Decimal

import pytest

from catalog.domain.entities import Cart, ProductInCart
from catalog.domain.value_objects import Quantity, UserID
from tests.factories import (
    CartFactory,
    PriceFactory,
    ProductFactory,
    ProductInCartFactory,
)


class TestCart:
    def test_cart_creation(self, cart: Cart):
        assert cart
        assert cart.id is None

    def test_cart_len(self, product_factory: ProductFactory):
        cart = Cart(user_id=UserID(1))
        assert len(cart) == 0
        cart.add_products(
            [
                ProductInCart(
                    product=product_factory.build(),
                    quantity=Quantity(1),
                )
            ]
        )
        assert len(cart) == 1

    @pytest.mark.parametrize(
        ("cart_id", "cart_user_id", "other_cart_id", "other_cart_user_id", "expected"),
        [
            (1, 1, 1, 1, True),
            (2, 1, 2, 1, True),
            (1, 2, 1, 2, True),
            (1, 1, 2, 2, False),
            (1, 1, 2, 1, False),
        ],
    )
    def test_cart_equal(
        self, cart_id, cart_user_id, other_cart_id, other_cart_user_id, expected
    ):
        cart = CartFactory.build(user_id=UserID(cart_user_id))
        other_cart = CartFactory.build(user_id=UserID(other_cart_user_id))
        cart.id = cart_id
        other_cart.id = other_cart_id
        eq = other_cart == cart
        assert eq == expected

    def test_cart_add_products(self, product_factory: ProductFactory):
        cart = Cart(user_id=UserID(1))
        new_product = ProductInCart(
            product=product_factory.build(),
            quantity=Quantity(1),
        )
        cart.add_products([new_product])
        assert cart.products == [new_product]

    def test_cart_remove_products(self, product_factory: ProductFactory):
        product1 = ProductInCart(
            product=product_factory.build(),
            quantity=Quantity(1),
        )
        product2 = ProductInCart(
            product=product_factory.build(),
            quantity=Quantity(1),
        )
        cart = Cart(user_id=UserID(1), products=[product1, product2])
        cart.remove_products([product1])
        assert cart.products == [product2]

    @pytest.mark.parametrize(
        ("products", "expected"),
        [
            ([], 0),
            (
                ProductInCartFactory.build_batch(
                    size=3,
                    product=ProductFactory.build(
                        price=PriceFactory.build(internal=Decimal(10))
                    ),
                ),
                30,
            ),
            (
                ProductInCartFactory.build_batch(
                    size=3,
                    product=ProductFactory.build(
                        price=PriceFactory.build(internal=Decimal(20))
                    ),
                ),
                60,
            ),
            (
                [
                    ProductInCartFactory.build(
                        product=ProductFactory.build(
                            price=PriceFactory.build(internal=Decimal(20))
                        ),
                    ),
                    ProductInCartFactory.build(
                        product=ProductFactory.build(
                            price=PriceFactory.build(internal=Decimal(50))
                        ),
                    ),
                ],
                70,
            ),
        ],
    )
    def test_cart_total_price(self, products, expected):
        cart = Cart(user_id=UserID(1), products=products)
        assert cart.total_price == expected

    @pytest.mark.parametrize(
        ("products", "expected"),
        [
            ([], 0),
            (
                ProductInCartFactory.build_batch(size=3, quantity=Quantity(10)),
                30,
            ),
            (
                ProductInCartFactory.build_batch(
                    size=1,
                    quantity=Quantity(10),
                ),
                10,
            ),
            (
                [
                    ProductInCartFactory.build(quantity=Quantity(10)),
                    ProductInCartFactory.build(quantity=Quantity(25)),
                ],
                35,
            ),
        ],
    )
    def test_cart_total_quantity(self, products, expected):
        cart = Cart(user_id=UserID(1), products=products)
        assert cart.total_quantity == expected
