from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest

from catalog.infrastructure.db.repos import CategoryRepoSQL


class TestCategoryRepo:
    @pytest.fixture
    def mock_entity(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def category_repo(self, session_mock, mock_entity) -> CategoryRepoSQL:
        repo = CategoryRepoSQL(session_mock)
        repo._entity = mock_entity
        return repo

    @pytest.mark.parametrize("id", [1, 15])
    async def test_get(
        self, category_repo: CategoryRepoSQL, session_mock, mock_entity, id
    ):
        await category_repo.get(id)
        session_mock.get.assert_awaited_once_with(mock_entity, id)

    @pytest.mark.parametrize("id", [0, -1])
    async def test_get_invalid_id(
        self, category_repo: CategoryRepoSQL, session_mock, id
    ):
        with pytest.raises(ValueError):
            await category_repo.get(id)
        session_mock.get.assert_not_awaited()

    async def test_list(
        self, mocker, category_repo: CategoryRepoSQL, session_mock, mock_entity
    ):
        mocker.patch(
            "catalog.infrastructure.db.repos.base.select", return_value=mock_entity
        )
        session_mock.stream_scalars.return_value = AsyncMock(return_value=[mock_entity])
        g = await category_repo.list()
        assert g is not None
        assert isinstance(g, AsyncGenerator)
        async for item in g:
            assert isinstance(item, mock_entity)
        session_mock.stream_scalars.assert_awaited_once()

    async def test_save(
        self, category_repo: CategoryRepoSQL, session_mock, mock_entity
    ):
        result = await category_repo.save(mock_entity)
        session_mock.add.assert_called_once_with(mock_entity)
        session_mock.refresh.assert_awaited_once_with(mock_entity)
        session_mock.flush.assert_awaited_once()
        assert not result
