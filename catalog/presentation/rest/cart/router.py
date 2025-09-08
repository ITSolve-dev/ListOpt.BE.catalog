from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from catalog.application.commands import (
    AddCartCommand,
    AddProductsToCartCommand,
    ChangeQuantitiesProductsInCartCommand,
    RemoveProductsFromCartCommand,
)
from catalog.application.queries import (
    GetCartByUserQuery,
)
from catalog.domain.exceptions import CartNotFoundError
from catalog.infrastructure.fastapi.dependencies import UserDep

from .schemas import (
    AddProductsToCartRequest,
    AddProductsToCartResponse,
    ChangeQuantitiesProductsRequest,
    ChangeQuantitiesProductsResponse,
    CreateCartResponse,
    DeleteProductsFromCartRequest,
    DeleteProductsFromCartResponse,
    GetMyCartResponse,
)

cart_router = APIRouter(prefix="/carts", tags=["Carts"])

GetCartByUser = Annotated[
    GetCartByUserQuery, Depends(Provide["get_cart_by_user_query"])
]
AddProductsToCart = Annotated[
    AddProductsToCartCommand, Depends(Provide["add_products_to_cart_command"])
]
RemoveProductsFromCart = Annotated[
    RemoveProductsFromCartCommand,
    Depends(Provide["remove_products_from_cart_command"]),
]
ChangeQuantitiesProducts = Annotated[
    ChangeQuantitiesProductsInCartCommand,
    Depends(Provide["change_quantities_products_in_cart_command"]),
]
AddCart = Annotated[AddCartCommand, Depends(Provide["add_cart_command"])]


@cart_router.get("/me")
@inject
async def get_my_cart(
    user: UserDep,
    get_cart_by_user: GetCartByUser,
) -> GetMyCartResponse:
    cart = await get_cart_by_user(user.id)
    if not cart:
        raise CartNotFoundError
    return GetMyCartResponse(cart=cart)


@cart_router.post("/products")
@inject
async def add_products_to_cart(
    user: UserDep,
    data: AddProductsToCartRequest,
    add_products_to_cart: AddProductsToCart,
) -> AddProductsToCartResponse:
    cart = await add_products_to_cart.execute(
        user.id, [(d.product_id, d.quantity) for d in data]
    )
    return AddProductsToCartResponse(cart=cart)


@cart_router.delete("/products")
@inject
async def delete_products_from_cart(
    user: UserDep,
    data: DeleteProductsFromCartRequest,
    remove_products_from_cart: RemoveProductsFromCart,
) -> DeleteProductsFromCartResponse:
    cart = await remove_products_from_cart.execute(user.id, data.product_ids)
    return DeleteProductsFromCartResponse(cart=cart)


@cart_router.patch("/products")
@inject
async def change_quantities_of_products(
    user: UserDep,
    data: ChangeQuantitiesProductsRequest,
    change_quantities_products_in_cart: ChangeQuantitiesProducts,
) -> ChangeQuantitiesProductsResponse:
    cart = await change_quantities_products_in_cart.execute(
        user.id, [(d.product_id, d.quantity) for d in data]
    )
    return ChangeQuantitiesProductsResponse(cart=cart)


@cart_router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def create_cart(
    user: UserDep,
    add_cart: AddCart,
) -> CreateCartResponse:
    cart = await add_cart.execute(user.id)
    return CreateCartResponse(cart=cart)
