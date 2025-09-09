from abc import ABC, abstractmethod
from typing import Any


class Interactor(ABC):
    @abstractmethod
    def execute(self, *_: Any, **__: Any) -> Any:
        pass


class Query(Interactor): ...


class Command(Interactor): ...
