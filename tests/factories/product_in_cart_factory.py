from factory.base import Factory
from factory.declarations import LazyFunction

from catalog.domain.entities import ProductInCart
from catalog.domain.value_objects import Quantity

from .faker import faker
from .mixins import IDMixin, TimestampMixin
from .product_factory import ProductFactory


class ProductInCartFactory(Factory[ProductInCart], TimestampMixin, IDMixin):
    class Meta:  # type: ignore
        model = ProductInCart

    product = LazyFunction(ProductFactory.create)
    quantity = LazyFunction(lambda: Quantity(faker.random_int(min=1, max=10)))
