from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from catalog.infrastructure.db.connection import DBConnection

DBConnectionMockTuple = tuple[DBConnection, MagicMock, MagicMock, MagicMock]


class TestDBConnection:
    @pytest.fixture
    def db_connection(self, mocker: MockerFixture) -> DBConnectionMockTuple:
        url = "sqlite:///:memory:"
        async_engine = mocker.MagicMock(spec=AsyncEngine)
        session = mocker.MagicMock(spec=AsyncSession)
        async_session_factory = mocker.MagicMock(
            spec=async_sessionmaker[AsyncSession], return_value=session
        )
        mocker.patch(
            "catalog.infrastructure.db.connection.create_async_engine",
            autospec=True,
            return_value=async_engine,
        )
        mocker.patch(
            "catalog.infrastructure.db.connection.async_sessionmaker",
            autospec=True,
            return_value=async_session_factory,
        )
        connection = DBConnection(
            url=url, config=dict(echo=False, max_overflow=5, pool_size=10)
        )
        return connection, session, async_session_factory, async_engine

    def test_init(self, mocker: MockerFixture):
        url = "sqlite:///:memory:"
        async_engine = mocker.MagicMock()
        create_async_engine = mocker.patch(
            "catalog.infrastructure.db.connection.create_async_engine",
            autospec=True,
            return_value=async_engine,
        )
        async_session_maker = mocker.patch(
            "catalog.infrastructure.db.connection.async_sessionmaker",
            autospec=True,
        )
        connection = DBConnection(
            url=url, config=dict(echo=False, max_overflow=5, pool_size=10)
        )
        create_async_engine.assert_called_once_with(
            url, echo=False, max_overflow=5, pool_size=10
        )
        async_session_maker.assert_called_once_with(
            async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
        assert connection
        assert not connection._session
        with pytest.raises(RuntimeError):
            assert connection.session

    async def test_handle_connection(
        self, db_connection: DBConnectionMockTuple
    ):
        connection, session, async_session_factory, _ = db_connection
        async with connection as local_session:
            async_session_factory.assert_called_once()
            assert connection.session
            assert local_session is connection.session
        assert not connection._session
        session.close.assert_called_once()
        with pytest.raises(RuntimeError):
            assert connection.session

    async def test_rollback_if_error(
        self, mocker: MockerFixture, db_connection: DBConnectionMockTuple
    ):
        connection, session, async_session_factory, _ = db_connection
        connection.commit = mocker.AsyncMock(
            side_effect=RuntimeError, return_value=session
        )

        async def flow() -> None:
            async with connection:
                async_session_factory.assert_called_once()
                await connection.commit()

        with pytest.raises(RuntimeError):
            await flow()
        session.close.assert_called_once()
        session.rollback.assert_called_once()
