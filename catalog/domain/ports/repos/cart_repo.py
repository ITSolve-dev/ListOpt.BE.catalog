from typing import Protocol

from catalog.domain.entities import Cart

from .abstract import AbstractRepo


class CartRepo(AbstractRepo[Cart], Protocol): ...
