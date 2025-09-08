from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from catalog.application.commands.add_cart_command import AddCartCommand
from catalog.application.commands.add_products_to_cart_command import (
    AddProductsToCartCommand,
)
from catalog.application.commands.change_quantities_products_in_cart_command import (
    ChangeQuantitiesProductsInCartCommand,
)
from catalog.application.commands.remove_products_from_cart_command import (
    RemoveProductsFromCartCommand,
)
from catalog.application.queries.get_cart_by_user_query import GetCartByUserQuery
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


@cart_router.get("/me")
@inject
async def get_my_cart(
    user: UserDep,
    get_cart_by_user_query: GetCartByUserQuery = Depends(
        Provide["get_cart_by_user_query"]
    ),
) -> GetMyCartResponse:
    cart = await get_cart_by_user_query(user.id)
    if not cart:
        raise CartNotFoundError
    return GetMyCartResponse(cart=cart)


@cart_router.post("/products")
@inject
async def add_products_to_cart(
    user: UserDep,
    data: AddProductsToCartRequest,
    add_products_to_cart_command: AddProductsToCartCommand = Depends(
        Provide["add_products_to_cart_command"]
    ),
) -> AddProductsToCartResponse:
    cart = await add_products_to_cart_command.execute(
        user.id, [(d.product_id, d.quantity) for d in data]
    )
    return AddProductsToCartResponse(cart=cart)


@cart_router.delete("/products")
@inject
async def delete_products_from_cart(
    user: UserDep,
    data: DeleteProductsFromCartRequest,
    remove_products_from_cart_command: RemoveProductsFromCartCommand = Depends(
        Provide["remove_products_from_cart_command"]
    ),
) -> DeleteProductsFromCartResponse:
    cart = await remove_products_from_cart_command.execute(user.id, data.product_ids)
    return DeleteProductsFromCartResponse(cart=cart)


@cart_router.patch("/products")
@inject
async def change_quantities_of_products(
    user: UserDep,
    data: ChangeQuantitiesProductsRequest,
    change_quantities_products_in_cart: ChangeQuantitiesProductsInCartCommand = Depends(
        Provide["change_quantities_products_in_cart"]
    ),
) -> ChangeQuantitiesProductsResponse:
    cart = await change_quantities_products_in_cart.execute(
        user.id, [(d.product_id, d.quantity) for d in data]
    )
    return ChangeQuantitiesProductsResponse(cart=cart)


@cart_router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def create_cart(
    user: UserDep,
    add_cart_command: AddCartCommand = Depends(Provide["add_cart_command"]),
) -> CreateCartResponse:
    cart = await add_cart_command.execute(user.id)
    return CreateCartResponse(cart=cart)
