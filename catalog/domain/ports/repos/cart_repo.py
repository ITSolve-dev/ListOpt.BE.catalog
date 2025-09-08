from typing import Protocol

from ...entities import Cart
from .abstract import AbstractRepo


class CartRepo(AbstractRepo[Cart], Protocol): ...
