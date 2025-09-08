from pydantic import BaseModel, TypeAdapter

from catalog.domain.entities import Product
from catalog.domain.ports.uow import AbstractUnitOfWork

ProductsFilteredOut = TypeAdapter(list[Product])


class PaginatedProducts(BaseModel):
    products: list[Product]
    page: int
    size: int
    total: int
    pages: int


class PaginateProductsQuery:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def __call__(
        self, *, page: int, page_size: int
    ) -> PaginatedProducts:
        async with self.uow:
            products = await self.uow.product_repo.paginate(page, page_size)
            total = await self.uow.product_repo.count()
            return PaginatedProducts(
                products=ProductsFilteredOut.validate_python(list(products)),
                page=page,
                size=page_size,
                total=total,
                pages=total // page_size + (total % page_size > 0),
            )
