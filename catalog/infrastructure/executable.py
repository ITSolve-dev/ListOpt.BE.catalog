from typing import Protocol


class ExecutableProtocol(Protocol):
    def run(self, *args, **kwargs) -> None: ...
