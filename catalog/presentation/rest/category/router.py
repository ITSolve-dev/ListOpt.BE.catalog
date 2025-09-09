from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from catalog.application.queries.get_categories_query import GetCategoriesQuery

from .schemas import GetCategoriesResponse

category_router = APIRouter(prefix="/categories", tags=["Categories"])

GetCategories = Annotated[
    GetCategoriesQuery, Depends(Provide["get_categories_query"])
]


@category_router.get("")
@inject
async def get_categories(
    get_categories: GetCategories,
) -> GetCategoriesResponse:
    categories = await get_categories.execute()
    return GetCategoriesResponse(categories=categories)
