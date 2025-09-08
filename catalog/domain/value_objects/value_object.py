from pydantic.dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValueObject: ...
