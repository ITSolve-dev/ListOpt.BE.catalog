from typing import Sequence

from ..entities import Category, Product, ProductField
from ..ports.uow import AbstractUnitOfWork
from ..value_objects import (
    CompanyID,
    Dimension,
    PositiveInt,
    Price,
    ProductIdentifier,
    ProductName,
    ProductPhoto,
)

# Добавить товары в корзину POST /carts/products
# Удалить товары из корзины DELETE /carts/products
# Изменять количество товара в корзине POST /carts/products/{id}
# Получить корзину пользователя GET /carts/me
# Создать корзину пользователя POST /carts
# Получить товар по id GET /products/{id}
# Добавить товар POST /products
# Редактировать товар PUT(PATCH) /products/{id}
# Фильтровать товары получить список + пагинация GET /products?query=<query>
# Получить категории GET /categories


class ProductService:
    def __init__(self, uow: AbstractUnitOfWork):
        self._uow = uow

    async def create_product(
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

    async def filter_products(self, *args, **kwargs) -> list[Product]: ...

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
