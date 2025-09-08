from typing import TypeVar, cast

from sqlalchemy.orm.attributes import InstrumentedAttribute

T = TypeVar("T")


def cast_inst_attr(field: T) -> InstrumentedAttribute[T]:
    return cast(InstrumentedAttribute[T], field)
