from catalog.domain.entities import Category
from catalog.domain.ports.repos import CategoryRepo

from .base import BaseRepoSQL


class CategoryRepoSQL(BaseRepoSQL[Category], CategoryRepo):
    _entity = Category
