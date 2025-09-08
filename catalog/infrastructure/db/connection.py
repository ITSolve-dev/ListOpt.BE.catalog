import logging
from abc import abstractmethod
from typing import Any, Protocol

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

logger = logging.getLogger(__name__)


class IDBConnection(Protocol):
    @abstractmethod
    async def __aenter__(self) -> AsyncSession: ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...

    @abstractmethod
    async def close(self): ...

    @property
    @abstractmethod
    def session(self) -> AsyncSession: ...

    @property
    @abstractmethod
    def session_factory(self) -> async_sessionmaker[AsyncSession]: ...


class DBConfig(BaseModel):
    echo: bool = False
    max_overflow: int = 5
    pool_size: int = 10


class DBConnection(IDBConnection):
    _session: AsyncSession | None
    _session_factory: async_sessionmaker[AsyncSession]
    _engine: AsyncEngine

    def __init__(self, url: str, config: dict[str, Any]):
        print(url)
        print(config)
        self._config = DBConfig.model_validate(config)
        self._engine = create_async_engine(
            url,
            echo=self._config.echo,
            max_overflow=self._config.max_overflow,
            pool_size=self._config.pool_size,
        )
        self._session_factory = async_sessionmaker(
            self._engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
        )
        self._session = None

    async def __aenter__(self):
        logger.debug("Open db connection")
        self._session = self._session_factory()
        return self._session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logger.debug("Rollback db connection cause %s", exc_val)
            await self.rollback()
        await self.close()
        logger.debug("Close db connection")

    async def close(self):
        await self.session.close()
        self._session = None

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError("Session is not initialized")
        return self._session

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory

    @property
    def engine(self) -> AsyncEngine:
        return self._engine
