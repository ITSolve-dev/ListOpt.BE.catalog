from contextlib import nullcontext
from decimal import Decimal

import pytest

from catalog.domain.value_objects import Price


class TestPrice:
    def test_price_creation(self, price: Price):
        assert price

    @pytest.mark.parametrize(
        "internal, external, expected",
        [
            (Decimal("0"), Decimal("0"), pytest.raises(ValueError)),
            (Decimal("1"), Decimal("1"), nullcontext()),
            (Decimal("100"), Decimal("100"), nullcontext()),
            (Decimal("123.21"), Decimal("342.34"), nullcontext()),
            (Decimal("12345678"), Decimal("12345678"), nullcontext()),
            (Decimal("12345678.91"), Decimal("12345678.91"), nullcontext()),
            (Decimal("123456789"), Decimal("123456789"), pytest.raises(ValueError)),
            (
                Decimal("12345678.912"),
                Decimal("12345678.912"),
                pytest.raises(ValueError),
            ),
            (Decimal("123.213"), Decimal("342.342"), pytest.raises(ValueError)),
            (Decimal("123.21312"), Decimal("342.34243"), pytest.raises(ValueError)),
            (Decimal("-1"), Decimal("100"), pytest.raises(ValueError)),
            (Decimal("100"), Decimal("-1"), pytest.raises(ValueError)),
            (Decimal("-1"), Decimal("-1"), pytest.raises(ValueError)),
        ],
    )
    def test_price_validation(self, internal: Decimal, external: Decimal, expected):
        with expected:
            Price(internal=internal, external=external)
