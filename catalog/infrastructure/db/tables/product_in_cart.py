from sqlalchemy import Column, ForeignKey, Integer, Table, UniqueConstraint

from .registry import mapper_registry
from .with_timestamp import with_timestamp

products_in_cart_table = with_timestamp(
    Table(
        "products_in_cart",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column(
            "cart_id",
            Integer,
            ForeignKey("carts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        Column(
            "product_id",
            Integer,
            ForeignKey("products.id", ondelete="CASCADE"),
            nullable=False,
        ),
        Column("quantity", Integer()),
        UniqueConstraint("product_id", "cart_id"),
    )
)
