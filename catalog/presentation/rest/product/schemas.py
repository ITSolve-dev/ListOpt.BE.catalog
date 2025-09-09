import json
from typing import Any

from pydantic import Field, model_validator

from catalog.domain.entities.product import Product
from catalog.presentation.rest._base_schemas import (
    PaginateResponse,
    RequestSchema,
    SuccessResponse,
)


class GetProductByIDResponse(SuccessResponse):
    info: str | None = "Get product by ID"
    product: Product


class AddProductRequest(RequestSchema):
    class ProductField(RequestSchema):
        name: str = Field(min_length=2, max_length=64)
        value: str = Field(min_length=2, max_length=64)
        measure: str = Field(min_length=2, max_length=64)

    company_id: int = Field(gt=0, examples=[1, 2])
    name: str = Field(
        min_length=2, max_length=100, examples=["milk", "cheese"]
    )
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
    fields: list[ProductField] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value: str | Any) -> "AddProductRequest":
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class AddProductResponse(SuccessResponse):
    info: str | None = "Product add"
    product: Product


class EditProductRequest(RequestSchema): ...


class EditProductResponse(SuccessResponse):
    info: str | None = "Product edit"


class PaginateProductsResponse(PaginateResponse[Product]):
    info: str | None = "Paginate products"
    items: list[Product] = Field(..., alias="products")
