from abc import abstractmethod
from typing import AsyncIterator, Protocol, Sequence


class AbstractRepo[EntityT](Protocol):
    @abstractmethod
    async def save(self, entity: EntityT) -> None: ...

    @abstractmethod
    async def get_by_ids(self, ids: list[int]) -> Sequence[EntityT]: ...

    @abstractmethod
    async def get(self, id: int) -> EntityT | None: ...

    @abstractmethod
    async def list(self) -> AsyncIterator[EntityT]: ...

    @abstractmethod
    async def count(self) -> int: ...

    @abstractmethod
    async def paginate(
        self, page: int, page_size: int
    ) -> Sequence[EntityT]: ...
