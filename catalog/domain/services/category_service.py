from catalog.domain.entities import Category
from catalog.domain.ports.uow import AbstractUnitOfWork


class CategoryService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow = uow

    async def get_category_by_id(self, category_id: int) -> Category | None:
        async with self._uow:
            return await self._uow.category_repo.get(category_id)
