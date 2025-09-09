from unittest.mock import AsyncMock

import pytest
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def session_mock(mocker: MockerFixture) -> AsyncMock:
    return mocker.AsyncMock(spec=AsyncSession)
