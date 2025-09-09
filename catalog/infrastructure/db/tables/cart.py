from sqlalchemy import Column, Integer, Table

from .registry import mapper_registry
from .with_timestamp import with_timestamp

carts_table = with_timestamp(
    Table(
        "carts",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("user_id", Integer, nullable=False),
    )
)
