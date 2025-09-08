from sqlalchemy.orm import joinedload, selectinload

from catalog.domain.entities import Cart, Product, ProductInCart
from catalog.domain.ports.repos.cart_repo import CartRepo
from catalog.infrastructure.db.helpers import cast_inst_attr

from .base import BaseRepoSQL


class CartRepoSQL(BaseRepoSQL[Cart], CartRepo):
    _entity = Cart

    async def _get(self, id: int) -> Cart | None:
        stmt = (
            self._base_select_stmt()
            .filter_by(user_id=id)
            .options(
                selectinload(cast_inst_attr(Cart.products))
                .joinedload(cast_inst_attr(ProductInCart.product))
                .options(
                    selectinload(cast_inst_attr(Product.fields)),
                    joinedload(cast_inst_attr(Product.category)),
                )
            )
        )
        cart = await self.session.scalar(stmt)
        return cart
