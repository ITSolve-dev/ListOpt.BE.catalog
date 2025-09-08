from sqlalchemy import Column, ForeignKey, Integer, String, Table

from .registry import mapper_registry
from .with_timestamp import with_timestamp

categories_table = with_timestamp(
    Table(
        "categories",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
        Column("parent_id", Integer, ForeignKey("categories.id"), nullable=True),
    )
)
