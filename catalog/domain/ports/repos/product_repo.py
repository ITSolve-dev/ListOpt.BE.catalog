from typing import Protocol

from catalog.domain.entities import Product

from .abstract import AbstractRepo


class ProductRepo(AbstractRepo[Product], Protocol): ...
