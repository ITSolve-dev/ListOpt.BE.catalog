from typing import Protocol

from catalog.domain.entities import Category

from .abstract import AbstractRepo


class CategoryRepo(AbstractRepo[Category], Protocol): ...
