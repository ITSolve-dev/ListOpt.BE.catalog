from catalog.domain.entities import Category
from catalog.domain.ports.uow import AbstractUnitOfWork


class GetCategoriesQuery:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def execute(self) -> list[Category]:
        async with self.uow:
            categories = await self.uow.category_repo.list()
            return [category async for category in categories]
