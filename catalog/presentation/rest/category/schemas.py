from catalog.domain.entities import Category
from catalog.presentation.rest._base_schemas import SuccessResponse


class GetCategoriesResponse(SuccessResponse):
    info: str | None = "Get categories"
    categories: list[Category]
