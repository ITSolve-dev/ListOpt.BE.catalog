from sqlalchemy.orm import composite, relationship

from catalog.domain.entities import Cart, Category, Product, ProductField, ProductInCart
from catalog.domain.value_objects import Dimension, Price, ProductIdentifier

from .tables import (
    carts_table,
    categories_table,
    mapper_registry,
    product_fields_table,
    products_in_cart_table,
    products_table,
)


def map_entities_on_tables():
    mapper_registry.map_imperatively(
        Cart,
        carts_table,
        properties={
            "products": relationship(
                ProductInCart, lazy="noload", cascade="all, delete-orphan"
            ),
        },
    )
    mapper_registry.map_imperatively(
        ProductInCart,
        products_in_cart_table,
        properties={
            "product": relationship(Product, lazy="noload", passive_deletes=True),
        },
    )
    mapper_registry.map_imperatively(
        ProductField,
        product_fields_table,
    )
    mapper_registry.map_imperatively(
        Product,
        products_table,
        properties={
            "category": relationship(Category, lazy="noload"),
            "fields": relationship(ProductField, lazy="noload"),
            "price": composite(
                Price, products_table.c.price_internal, products_table.c.price_external
            ),
            "dimension": composite(
                Dimension,
                products_table.c.width,
                products_table.c.height,
                products_table.c.depth,
                products_table.c.weight,
            ),
            "identifier": composite(
                ProductIdentifier,
                products_table.c.article,
                products_table.c.barcode,
            ),
        },
    )
    mapper_registry.map_imperatively(
        Category,
        categories_table,
        properties={
            "parent": relationship(
                Category,
                back_populates="children",
                uselist=False,
                lazy="noload",
                default=None,
                join_depth=1,
                remote_side=[categories_table.c.id],
            ),
            "children": relationship(
                Category,
                back_populates="parent",
                lazy="noload",
                default_factory=list,
                join_depth=1,
            ),
        },
    )
