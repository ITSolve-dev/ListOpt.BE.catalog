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
