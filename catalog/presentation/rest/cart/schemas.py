from pydantic import Field

from catalog.domain.entities import Cart

from .._base_schemas import RequestSchema, SuccessResponse


class GetMyCartResponse(SuccessResponse):
    info: str | None = "Cart retrieve"
    cart: Cart


class AddProductToCartRequest(RequestSchema):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


AddProductsToCartRequest = list[AddProductToCartRequest]


class AddProductsToCartResponse(SuccessResponse):
    info: str | None = "Add products to cart"
    cart: Cart


class DeleteProductsFromCartRequest(RequestSchema):
    product_ids: list[int]


class DeleteProductsFromCartResponse(SuccessResponse):
    info: str | None = "Delete products to cart"
    cart: Cart


class CreateCartResponse(SuccessResponse):
    info: str | None = "Cart create"
    cart: Cart


class ChangeQuantityProductRequest(RequestSchema):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


ChangeQuantitiesProductsRequest = list[ChangeQuantityProductRequest]


class ChangeQuantitiesProductsResponse(SuccessResponse):
    cart: Cart
    info: str | None = "Change quantity of products in cart"
