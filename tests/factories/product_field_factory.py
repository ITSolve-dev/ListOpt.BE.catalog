from factory.base import Factory
from factory.declarations import LazyFunction

from catalog.domain.entities import ProductField
from catalog.domain.value_objects import PositiveInt

from .attributes import ValueObjectIntSequence
from .faker import faker
from .mixins import IDMixin, TimestampMixin


class ProductFieldFactory(IDMixin, TimestampMixin, Factory[ProductField]):
    class Meta:  # type: ignore
        model = ProductField

    name = LazyFunction(faker.name)
    value = LazyFunction(faker.name)
    measure = LazyFunction(faker.name)
    product_id = ValueObjectIntSequence(PositiveInt)
