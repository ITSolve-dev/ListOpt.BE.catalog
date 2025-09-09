from typing import Any, Protocol


class ExecutableProtocol(Protocol):
    def run(self, *args: Any, **kwargs: Any) -> None: ...
