from typing import Annotated

from pydantic import AfterValidator, Field, HttpUrl
from pydantic.dataclasses import dataclass

from ..value_objects import (
    CompanyID,
    Dimension,
    PositiveInt,
    Price,
    ProductIdentifier,
    ProductName,
    ProductPhoto,
)
from .category import Category
from .entity import Entity
from .product_field import ProductField

ListOptS3Url = Annotated[
    HttpUrl, AfterValidator(lambda url: url.startswith("https://"))
]


@dataclass(kw_only=True)
class Product(Entity):
    company_id: CompanyID = Field(gt=0)
    name: ProductName = Field(min_length=2, max_length=100)
    identifier: ProductIdentifier = Field()
    price: Price = Field()
    amount: PositiveInt = Field(gt=0)
    dimension: Dimension = Field()
    category: Category = Field()
    description: str | None = Field(default=None, max_length=255)
    photo: ProductPhoto | None = Field(default=None)
    fields: list[ProductField] = Field(default_factory=list)

    @classmethod
    def create(
        cls,
        *,
        company_id: CompanyID,
        name: ProductName,
        identifier: ProductIdentifier,
        price: Price,
        amount: PositiveInt,
        dimension: Dimension,
        category: Category,
        description: str | None = None,
        photo: ProductPhoto | None = None,
        fields: list[ProductField] | None = None,
    ) -> "Product":
        if not fields:
            fields = []
        return Product(
            company_id=company_id,
            name=name,
            identifier=identifier,
            price=price,
            amount=amount,
            dimension=dimension,
            photo=photo,
            description=description,
            fields=fields,
            category=category,
        )
