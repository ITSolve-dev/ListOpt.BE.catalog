from typing import Sequence

from catalog.domain.entities import Category, Product, ProductField
from catalog.domain.ports.uow import AbstractUnitOfWork
from catalog.domain.value_objects import (
    CompanyID,
    Dimension,
    PositiveInt,
    Price,
    ProductIdentifier,
    ProductName,
    ProductPhoto,
)


class ProductService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow = uow

    async def create_product(  # noqa: PLR0913
        self,
        *,
        company_id: CompanyID,
        name: ProductName,
        identifier: ProductIdentifier,
        price: Price,
        amount: PositiveInt,
        dimension: Dimension,
        category: Category,
        description: str | None = None,
        photo: ProductPhoto | None = None,
        fields: list[ProductField] | None = None,
    ) -> Product:
        product = Product.create(
            company_id=company_id,
            name=name,
            identifier=identifier,
            price=price,
            amount=amount,
            dimension=dimension,
            photo=photo,
            description=description,
            fields=fields,
            category=category,
        )
        async with self._uow:
            await self._uow.product_repo.save(product)
        return product

    async def get_by_id(self, product_id: int) -> Product | None:
        async with self._uow:
            return await self._uow.product_repo.get(product_id)

    async def get_by_ids(self, product_ids: list[int]) -> Sequence[Product]:
        async with self._uow:
            return await self._uow.product_repo.get_by_ids(product_ids)

    async def get(self, product: Product) -> Product | None:
        if not product.id:
            raise RuntimeError("Product does not have ID")
        async with self._uow:
            return await self._uow.product_repo.get(product.id)
