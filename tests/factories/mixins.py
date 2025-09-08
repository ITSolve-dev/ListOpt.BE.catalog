from __future__ import annotations

import datetime

from factory.declarations import LazyFunction

from .attributes import IDSequence


class TimestampMixin:
    created_at = LazyFunction(lambda: datetime.datetime.now(datetime.UTC))
    updated_at = LazyFunction(lambda: datetime.datetime.now(datetime.UTC))


class IDMixin:
    id = IDSequence
