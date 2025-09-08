from typing import cast

from sqlalchemy.orm.attributes import InstrumentedAttribute


def cast_inst_attr[T](field: T) -> InstrumentedAttribute[T]:
    return cast(InstrumentedAttribute[T], field)
