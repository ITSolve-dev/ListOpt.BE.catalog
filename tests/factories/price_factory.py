from factory.base import Factory
from factory.declarations import LazyAttribute

from catalog.domain.value_objects import Price

from .faker import faker
from .mixins import IDMixin, TimestampMixin


class PriceFactory(Factory[Price], TimestampMixin, IDMixin):
    class Meta:  # type: ignore
        model = Price

    internal = LazyAttribute(lambda _: float(faker.random_int(min=100, max=10000)))
    external = LazyAttribute(lambda _: float(faker.random_int(min=100, max=10000)))
