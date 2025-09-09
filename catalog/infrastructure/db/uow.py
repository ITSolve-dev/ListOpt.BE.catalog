import logging
from types import TracebackType
from typing import Self

from catalog.domain.ports.uow import AbstractUnitOfWork

from .connection import IDBConnection
from .repos import CartRepoSQL, CategoryRepoSQL, ProductRepoSQL

logger = logging.getLogger(__name__)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    _db_connection: IDBConnection

    def __init__(self, db_connection: IDBConnection) -> None:
        self._db_connection = db_connection

    async def __aenter__(self) -> Self:
        await self._db_connection.__aenter__()
        self._db_connection.session.begin()
        self.cart_repo = CartRepoSQL(self._db_connection.session)
        self.product_repo = ProductRepoSQL(self._db_connection.session)
        self.category_repo = CategoryRepoSQL(self._db_connection.session)
        return await super().__aenter__()

    async def __aexit__(
        self,
        exc_type: type[Exception],
        exc_val: Exception,
        exc_tb: TracebackType,
    ) -> None:
        await self.commit()
        await self._db_connection.__aexit__(exc_type, exc_val, exc_tb)
        logger.info("Exiting UnitOfWork")

    async def commit(self) -> None:
        await self._db_connection.commit()

    async def rollback(self) -> None:
        await self._db_connection.rollback()
