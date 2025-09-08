import random

from factory.base import Factory
from factory.declarations import LazyFunction

from catalog.domain.entities import Cart
from catalog.domain.value_objects import UserID

from .attributes import ValueObjectIntSequence
from .mixins import IDMixin, TimestampMixin
from .product_in_cart_factory import ProductInCartFactory


def generate_products():
    return [ProductInCartFactory.create() for _ in range(random.randint(0, 10))]


class CartFactory(TimestampMixin, IDMixin, Factory[Cart]):
    class Meta:  # type: ignore
        model = Cart

    user_id = ValueObjectIntSequence(UserID)
    products = LazyFunction(generate_products)
