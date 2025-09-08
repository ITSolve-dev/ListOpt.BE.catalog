from pytest_mock import MockerFixture

from catalog.infrastructure.db.repos import CartRepoSQL, CategoryRepoSQL, ProductRepoSQL
from catalog.infrastructure.db.uow import SqlAlchemyUnitOfWork


class TestSQLAlchemyUnitOfWork:
    def test_uow_creation(self, mocker: MockerFixture):
        db_connection_mock = mocker.AsyncMock()
        uow = SqlAlchemyUnitOfWork(db_connection_mock)
        assert uow

    async def test_handle_context_manager(self, mocker: MockerFixture):
        db_connection_mock = mocker.AsyncMock()
        uow = SqlAlchemyUnitOfWork(db_connection_mock)
        cart_repo_init = mocker.patch.object(CartRepoSQL, "__init__", return_value=None)
        category_repo_init = mocker.patch.object(
            CategoryRepoSQL, "__init__", return_value=None
        )
        product_repo_init = mocker.patch.object(
            ProductRepoSQL, "__init__", return_value=None
        )
        async with uow:
            db_connection_mock.__aenter__.assert_awaited_once()
            db_connection_mock.session.begin.assert_called_once()
            cart_repo_init.assert_called_once_with(db_connection_mock.session)
            category_repo_init.assert_called_once_with(db_connection_mock.session)
            product_repo_init.assert_called_once_with(db_connection_mock.session)
            assert uow.cart_repo
            assert uow.product_repo
            assert uow.category_repo
        db_connection_mock.commit.assert_awaited_once()
        db_connection_mock.__aexit__.assert_awaited_once()
