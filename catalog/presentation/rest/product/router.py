from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, File, Query, UploadFile

from catalog.application.commands.add_product_command import (
    AddProductCommand,
    AddProductDTO,
)
from catalog.application.queries.get_product_query import GetProductQuery
from catalog.application.queries.paginate_products_query import (
    PaginateProductsQuery,
)

from .schemas import (
    AddProductRequest,
    AddProductResponse,
    EditProductRequest,
    EditProductResponse,
    GetProductByIDResponse,
    PaginateProductsResponse,
)

product_router = APIRouter(prefix="/products", tags=["Products"])


@product_router.get("/{product_id}")
@inject
async def get_product_by_id(
    product_id: int,
    get_product_query: GetProductQuery = Depends(Provide["get_product_query"]),
) -> GetProductByIDResponse:
    product = await get_product_query(product_id)
    if not product:
        raise ValueError
    return GetProductByIDResponse(product=product)


@product_router.post("")
@inject
async def add_product(
    data: AddProductRequest = Body(...),
    photo: UploadFile = File(...),
    add_product_command: AddProductCommand = Depends(
        Provide["add_product_command"]
    ),
) -> AddProductResponse:
    product = await add_product_command(
        AddProductDTO.model_validate(data.model_dump())
    )
    return AddProductResponse(product=product)


@product_router.patch("/{product_id}")
@inject
async def edit_product(
    product_id: int,
    data: EditProductRequest,
) -> EditProductResponse:
    return EditProductResponse()


@product_router.get("")
@inject
async def paginate_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=1000, alias="pageSize"),
    paginate_products_query: PaginateProductsQuery = Depends(
        Provide["paginate_products_query"]
    ),
) -> PaginateProductsResponse:
    result = await paginate_products_query(page=page, page_size=page_size)
    return PaginateProductsResponse.model_validate(result)
