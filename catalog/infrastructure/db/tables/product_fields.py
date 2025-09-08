from sqlalchemy import Column, ForeignKey, Integer, String, Table

from .registry import mapper_registry
from .with_timestamp import with_timestamp

product_fields_table = with_timestamp(
    Table(
        "product_fields",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("product_id", Integer, ForeignKey("products.id"), nullable=False),
        Column("name", String(50)),
        Column("value", String(50)),
        Column("measure", String(50)),
    )
)
