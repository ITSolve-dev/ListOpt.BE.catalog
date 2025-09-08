from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest
from pytest_mock import MockerFixture

from catalog.infrastructure.db.repos import CartRepoSQL


class TestCartRepo:
    @pytest.fixture
    def mock_entity(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def cart_repo(self, session_mock: AsyncMock) -> CartRepoSQL:
        repo = CartRepoSQL(session_mock)
        return repo

    @pytest.mark.parametrize("id", [1, 15])
    async def test_get(
        self,
        mocker: MockerFixture,
        cart_repo: CartRepoSQL,
        session_mock: AsyncMock,
        id: int,
    ):
        mocker.patch(
            "catalog.infrastructure.db.repos.cart_repo.joinedload",
        )
        mocker.patch(
            "catalog.infrastructure.db.repos.cart_repo.selectinload",
        )
        filter_by_mock = mocker.MagicMock()
        select_stmt = mocker.MagicMock()
        select_stmt.filter_by = filter_by_mock
        cart_repo._base_select_stmt = mocker.MagicMock(
            return_value=select_stmt
        )
        await cart_repo.get(id)
        cart_repo._base_select_stmt.assert_called_once()
        filter_by_mock.assert_called_once_with(user_id=id)
        session_mock.scalar.assert_awaited_once()

    @pytest.mark.parametrize("id", [0, -1])
    async def test_get_invalid_id(
        self, cart_repo: CartRepoSQL, session_mock: AsyncMock, id: int
    ):
        with pytest.raises(ValueError, match="greater than 0"):
            await cart_repo.get(id)
        session_mock.get.assert_not_awaited()

    async def test_list(
        self,
        mocker: MockerFixture,
        cart_repo: CartRepoSQL,
        session_mock: AsyncMock,
        mock_entity: MagicMock,
    ):
        mocker.patch(
            "catalog.infrastructure.db.repos.base.select",
            return_value=mock_entity,
        )
        session_mock.stream_scalars.return_value = AsyncMock(
            return_value=[mock_entity]
        )
        g = await cart_repo.list()
        assert g is not None
        assert isinstance(g, AsyncGenerator)
        async for item in g:
            assert isinstance(item, mock_entity)
        session_mock.stream_scalars.assert_awaited_once()

    async def test_save(
        self,
        cart_repo: CartRepoSQL,
        session_mock: AsyncMock,
        mock_entity: MagicMock,
    ):
        result = await cart_repo.save(mock_entity)
        session_mock.add.assert_called_once_with(mock_entity)
        session_mock.refresh.assert_awaited_once_with(mock_entity)
        session_mock.flush.assert_awaited_once()
        assert not result
