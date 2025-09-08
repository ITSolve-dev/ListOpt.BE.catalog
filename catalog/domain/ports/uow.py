import logging
from abc import ABC, abstractmethod
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

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.commit()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError
