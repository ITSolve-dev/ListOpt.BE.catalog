from sqlalchemy import Select
from sqlalchemy.orm import selectinload

from catalog.domain.entities import Product
from catalog.domain.ports.repos import ProductRepo
from catalog.infrastructure.db.helpers import cast_inst_attr

from .base import BaseRepoSQL


class ProductRepoSQL(BaseRepoSQL[Product], ProductRepo):
    _entity = Product

    async def _get(self, id: int) -> Product | None:
        stmt = (
            self._base_select_stmt()
            .filter_by(id=id)
            .options(
                selectinload(cast_inst_attr(Product.category)),
                selectinload(cast_inst_attr(Product.fields)),
            )
        )
        return await self.session.scalar(stmt)

    def _pagination_stmt(
        self, page: int, page_size: int
    ) -> Select[tuple[Product]]:
        offset = (page - 1) * page_size
        stmt = (
            self._base_select_stmt()
            .options(
                selectinload(cast_inst_attr(Product.category)),
                selectinload(cast_inst_attr(Product.fields)),
            )
            .offset(offset)
            .limit(page_size)
        )
        return stmt
