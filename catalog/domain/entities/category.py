from typing import Self

from pydantic import Field
from pydantic.dataclasses import dataclass

from ..value_objects import CategoryName
from .entity import Entity


@dataclass(kw_only=True)
class Category(Entity):
    name: CategoryName = Field(min_length=1, max_length=100)
    parent: Self | None = Field(default=None)
    children: list[Self] = Field(default_factory=list)
