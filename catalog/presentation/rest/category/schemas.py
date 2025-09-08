from catalog.domain.entities import Category

from .._base_schemas import SuccessResponse


class GetCategoriesResponse(SuccessResponse):
    info: str | None = "Get categories"
    categories: list[Category]
