from pytest_factoryboy import register

from .factories import (
    CartFactory,
    CategoryFactory,
    DimensionFactory,
    PriceFactory,
    ProductFactory,
    ProductFieldFactory,
    ProductIdentifierFactory,
    ProductInCartFactory,
)

register(CartFactory)
register(ProductInCartFactory)
register(CategoryFactory)
register(DimensionFactory)
register(ProductFactory)
register(ProductFieldFactory)
register(ProductIdentifierFactory)
register(PriceFactory)
