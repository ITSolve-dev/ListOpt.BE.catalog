from ..entities import Category
from ..ports.uow import AbstractUnitOfWork


class CategoryService:
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow

    async def get_category_by_id(self, category_id: int) -> Category | None:
        async with self._uow:
            return await self._uow.category_repo.get(category_id)
