from factory.base import Factory
from factory.declarations import LazyAttribute

from catalog.domain.value_objects import ProductIdentifier

from .faker import faker
from .mixins import IDMixin, TimestampMixin


class ProductIdentifierFactory(
    Factory[ProductIdentifier], TimestampMixin, IDMixin
):
    class Meta:  # type: ignore
        model = ProductIdentifier

    article = LazyAttribute(
        lambda _: str(faker.random_int(min=100000, max=999999))
    )
    barcode = LazyAttribute(
        lambda _: str(faker.random_int(min=100000, max=999999))
    )
