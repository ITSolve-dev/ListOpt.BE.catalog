from factory.base import Factory
from factory.declarations import LazyAttribute

from catalog.domain.value_objects import Dimension

from .faker import faker
from .mixins import IDMixin, TimestampMixin


class DimensionFactory(Factory[Dimension], TimestampMixin, IDMixin):
    class Meta:  # type: ignore
        model = Dimension

    width = LazyAttribute(
        lambda _: float(faker.random_int(min=100, max=10000))
    )
    height = LazyAttribute(
        lambda _: float(faker.random_int(min=100, max=10000))
    )
    depth = LazyAttribute(
        lambda _: float(faker.random_int(min=100, max=10000))
    )
    weight = LazyAttribute(
        lambda _: float(faker.random_int(min=100, max=10000))
    )
