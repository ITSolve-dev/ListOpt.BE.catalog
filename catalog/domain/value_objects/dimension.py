from typing import Annotated

from pydantic import Field
from pydantic.dataclasses import dataclass

from .value_object import ValueObject

DimensionField = Annotated[float, Field(gt=0)]


@dataclass(frozen=True, slots=True)
class Dimension(ValueObject):
    width: DimensionField
    height: DimensionField
    depth: DimensionField
    weight: DimensionField

    @property
    def volume(self) -> float:
        return self.width * self.height * self.depth
