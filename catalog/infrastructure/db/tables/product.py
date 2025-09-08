from sqlalchemy import DECIMAL, Column, Float, ForeignKey, Integer, String, Table

from .registry import mapper_registry
from .with_timestamp import with_timestamp

products_table = with_timestamp(
    Table(
        "products",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("company_id", Integer, nullable=False),
        Column("name", String(50)),
        Column("article", String(50)),
        Column("barcode", String(12)),
        Column("price_internal", DECIMAL(10, 2)),
        Column("price_external", DECIMAL(10, 2)),
        Column("amount", Integer),
        Column("description", String(255)),
        Column("photo", String(255)),
        Column("width", Float(2)),
        Column("height", Float(2)),
        Column("depth", Float(2)),
        Column("weight", Float(2)),
        Column("category_id", Integer, ForeignKey("categories.id"), nullable=False),
    )
)
