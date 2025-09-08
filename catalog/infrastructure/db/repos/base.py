from typing import AsyncIterator, Sequence

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import TypedReturnsRows

from catalog.domain.entities.entity import Entity
from catalog.infrastructure.db.helpers import cast_inst_attr


class BaseRepoSQL[EntityT: Entity]:
    _entity: type[EntityT]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _save(self, entity: EntityT) -> None:
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)

    async def _get(self, id: int) -> EntityT | None:
        stmt = self._base_select_stmt().filter_by(id=id)
        return await self.session.scalar(stmt)

    async def _list(self) -> AsyncIterator[EntityT]:
        result = await self.session.stream_scalars(self._base_select_stmt())
        async for entity in result:
            yield entity

    def _base_select_stmt(self) -> Select[tuple[EntityT]]:
        return select(self._entity)

    def _pagination_stmt(
        self, page: int, page_size: int
    ) -> Select[tuple[EntityT]]:
        offset = (page - 1) * page_size
        stmt = self._base_select_stmt().offset(offset).limit(page_size)
        return stmt

    async def _scalars(
        self, stmt: TypedReturnsRows[tuple[EntityT]]
    ) -> Sequence[EntityT]:
        result = await self.session.scalars(stmt)
        return result.unique().all()

    async def save(self, entity: EntityT) -> None:
        await self._save(entity)

    async def get(self, id: int) -> EntityT | None:
        if id < 1:
            raise ValueError("Invalid ID - must be greater than 0")
        return await self._get(id)

    async def get_by_ids(self, ids: list[int]) -> Sequence[EntityT]:
        stmt = self._base_select_stmt().where(
            cast_inst_attr(self._entity.id).in_(ids)
        )
        return await self._scalars(stmt)

    async def list(self) -> AsyncIterator[EntityT]:
        return self._list()

    async def count(self) -> int:
        stmt = select(func.count()).select_from(self._entity)
        count = await self.session.scalar(stmt) or 0
        return count

    async def paginate(self, page: int, page_size: int) -> Sequence[EntityT]:
        stmt = self._pagination_stmt(page, page_size)
        return await self._scalars(stmt)
