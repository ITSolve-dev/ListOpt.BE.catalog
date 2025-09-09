from catalog.domain.entities import Product
from catalog.domain.ports.uow import AbstractUnitOfWork


class GetProductQuery:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, product_id: int) -> Product | None:
        async with self.uow:
            product = await self.uow.product_repo.get(product_id)
            return product
