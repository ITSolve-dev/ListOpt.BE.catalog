from typing import Protocol

from ...entities import Category
from .abstract import AbstractRepo


class CategoryRepo(AbstractRepo[Category], Protocol): ...
