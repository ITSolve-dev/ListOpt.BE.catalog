from typing import Protocol

from ...entities import Product
from .abstract import AbstractRepo


class ProductRepo(AbstractRepo[Product], Protocol): ...
