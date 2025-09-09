import logging
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, File, Query, UploadFile

from catalog.application.commands.add_product_command import (
    AddProductCommand,
    AddProductDTO,
)
from catalog.application.queries import (
    GetProductQuery,
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

logger = logging.getLogger(__name__)

product_router = APIRouter(prefix="/products", tags=["Products"])

GetProduct = Annotated[GetProductQuery, Depends(Provide["get_product_query"])]
AddProduct = Annotated[
    AddProductCommand, Depends(Provide["add_product_command"])
]
PaginateProducts = Annotated[
    PaginateProductsQuery, Depends(Provide["paginate_products_query"])
]


@product_router.get("/{product_id}")
@inject
async def get_product_by_id(
    product_id: int,
    get_product: GetProduct,
) -> GetProductByIDResponse:
    product = await get_product(product_id)
    if not product:
        raise ValueError
    return GetProductByIDResponse(product=product)


@product_router.post("")
@inject
async def add_product(
    add_product: AddProduct,
    data: AddProductRequest = Body(...),
    photo: UploadFile = File(...),
) -> AddProductResponse:
    logger.debug(photo)
    product = await add_product(
        AddProductDTO.model_validate(data.model_dump())
    )
    return AddProductResponse(product=product)


@product_router.patch("/{product_id}")
@inject
async def edit_product(
    product_id: int,
    _: EditProductRequest,
) -> EditProductResponse:
    return EditProductResponse(info=f"{product_id} Coming Soon")


@product_router.get("")
@inject
async def paginate_products(
    paginate_products: PaginateProducts,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=1000, alias="pageSize"),
) -> PaginateProductsResponse:
    result = await paginate_products(page=page, page_size=page_size)
    return PaginateProductsResponse.model_validate(result)
