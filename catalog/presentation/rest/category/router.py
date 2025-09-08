from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from catalog.application.queries.get_categories_query import GetCategoriesQuery

from .schemas import GetCategoriesResponse

category_router = APIRouter(prefix="/categories", tags=["Categories"])


@category_router.get("")
@inject
async def get_categories(
    get_categories_query: GetCategoriesQuery = Depends(
        Provide["get_categories_query"]
    ),
) -> GetCategoriesResponse:
    categories = await get_categories_query()
    return GetCategoriesResponse(categories=categories)
