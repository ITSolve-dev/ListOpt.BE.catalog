from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, kw_only=True, slots=True)
class BaseError(Exception):
    app: str
    error: str
    ctx: dict[str, Any] | None = field(default=None)
    description: str | None = field(default=None)

    def __str__(self) -> str:
        return self.description or self.__class__.__name__

    @property
    def code(self) -> str:
        return f"{self.app}.{self.layer}.{self.error}"

    @property
    @abstractmethod
    def layer(self) -> str: ...
