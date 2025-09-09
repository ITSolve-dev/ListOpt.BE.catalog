import logging
from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from .repos import CartRepo, CategoryRepo, ProductRepo

logger = logging.getLogger(__name__)


class AbstractUnitOfWork(ABC):
    cart_repo: CartRepo
    product_repo: ProductRepo
    category_repo: CategoryRepo

    async def __aenter__(self) -> Self:
        logger.info("Entering unit of work")
        return self

    async def __aexit__(
        self,
        exc_type: type[Exception],
        exc_val: Exception,
        exc_tb: TracebackType,
    ) -> None:
        await self.commit()

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
