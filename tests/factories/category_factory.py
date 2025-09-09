import random

from factory.base import Factory
from factory.declarations import LazyFunction

from catalog.domain.entities import Category
from catalog.domain.value_objects import CategoryName

from .faker import faker
from .mixins import IDMixin, TimestampMixin


def generate_parent():
    return CategoryFactory.create() if random.choice([True, False]) else None


class CategoryFactory(Factory[Category], TimestampMixin, IDMixin):
    class Meta:  # type: ignore
        model = Category

    name = LazyFunction(lambda: CategoryName(faker.name()))
    children = []
    parent = LazyFunction(generate_parent)
