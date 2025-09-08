import datetime

from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass


@dataclass(kw_only=True, config=ConfigDict(arbitrary_types_allowed=True))
class Entity:
    id: int | None = Field(default=None, init=False, gt=0)
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        init=False,
    )
    updated_at: datetime.datetime | None = Field(default=None, init=False)

    @property
    def persisted(self) -> bool:
        return self.id is not None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
