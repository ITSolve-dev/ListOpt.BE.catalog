from decimal import Decimal

from pydantic import BaseModel, Field

from catalog.domain.entities import Product, ProductField
from catalog.domain.exceptions import CategoryNotFoundError, ProductNotFoundError
from catalog.domain.ports.uow import AbstractUnitOfWork
from catalog.domain.services import CategoryService, ProductService
from catalog.domain.value_objects import (
    CompanyID,
    Dimension,
    PositiveInt,
    Price,
    ProductIdentifier,
    ProductName,
)


class AddProductDTO(BaseModel):
    class ProductFieldDTO(BaseModel):
        name: str = Field(min_length=2, max_length=64)
        value: str = Field(min_length=2, max_length=64)
        measure: str = Field(min_length=2, max_length=64)

    company_id: int = Field(gt=0, examples=[1, 2])
    name: str = Field(min_length=2, max_length=100, examples=["milk", "cheese"])
    article: str = Field(min_length=1, max_length=15, examples=["123456789"])
    barcode: str = Field(min_length=1, max_length=15, examples=["123456789"])
    price_internal: float = Field(gt=0, examples=[1.23])
    price_external: float = Field(gt=0, examples=[1.23])
    amount: int = Field(gt=0)
    width: float = Field(gt=0)
    height: float = Field(gt=0)
    depth: float = Field(gt=0)
    weight: float = Field(gt=0)
    category_id: int = Field(gt=0)
    description: str | None = Field(default=None, max_length=255)
    fields: list[ProductFieldDTO] = Field(default_factory=list)


class AddProductCommand:
    _uow: AbstractUnitOfWork

    def __init__(
        self, product_service: ProductService, category_service: CategoryService
    ):
        self._product_service = product_service
        self._category_service = category_service

    async def __call__(self, data: AddProductDTO) -> Product:
        category = await self._category_service.get_category_by_id(data.category_id)
        if not category:
            raise CategoryNotFoundError
        new_product = await self._product_service.create_product(
            company_id=CompanyID(data.company_id),
            name=ProductName(data.name),
            identifier=ProductIdentifier(
                article=data.article,
                barcode=data.barcode,
            ),
            price=Price(
                internal=Decimal(str(data.price_internal)),
                external=Decimal(str(data.price_external)),
            ),
            amount=PositiveInt(data.amount),
            dimension=Dimension(
                width=data.width,
                height=data.height,
                weight=data.weight,
                depth=data.depth,
            ),
            description=data.description,
            fields=[
                ProductField(
                    name=field.name,
                    value=field.value,
                    measure=field.measure,
                )
                for field in data.fields
            ],
            category=category,
        )
        product = await self._product_service.get(new_product)
        if not product:
            raise ProductNotFoundError
        return product
