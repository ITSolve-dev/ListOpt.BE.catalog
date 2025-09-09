import random

from factory.base import Factory
from factory.declarations import (
    LazyAttribute,
    LazyFunction,
    SubFactory,
)

from catalog.domain.entities import Product
from catalog.domain.value_objects import (
    CompanyID,
    PositiveInt,
    ProductName,
    ProductPhoto,
)

from .attributes import IDSequence, ValueObjectIntSequence
from .category_factory import CategoryFactory
from .dimension_factory import DimensionFactory
from .faker import faker
from .mixins import TimestampMixin
from .price_factory import PriceFactory
from .product_field_factory import ProductFieldFactory
from .product_identifier_factory import ProductIdentifierFactory


def generate_fields(product: "ProductFactory") -> list:
    return [
        ProductFieldFactory.create(product_id=product.id)
        for _ in range(random.randint(0, 10))
    ]


class ProductFactory(TimestampMixin, Factory[Product]):
    class Meta:  # type: ignore
        model = Product

    id = IDSequence
    company_id = ValueObjectIntSequence(CompanyID)
    name = LazyFunction(lambda: ProductName(faker.name()))
    identifier = SubFactory(ProductIdentifierFactory)
    price = SubFactory(PriceFactory)
    amount = LazyFunction(
        lambda: PositiveInt(faker.random_int(min=1, max=10000))
    )
    description = LazyFunction(faker.text)
    photo = LazyFunction(lambda: ProductPhoto(faker.url()))
    dimension = SubFactory(DimensionFactory)
    fields = LazyAttribute(generate_fields)
    category = SubFactory(CategoryFactory)
