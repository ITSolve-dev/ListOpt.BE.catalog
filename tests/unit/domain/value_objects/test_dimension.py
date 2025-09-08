from contextlib import nullcontext

import pytest

from catalog.domain.value_objects import Dimension


class TestDimension:
    def test_dimension_creation(self, dimension: Dimension):
        assert dimension

    @pytest.mark.parametrize(
        "width, height, weight, depth, expected",
        [
            (1, 2, 3, 4, nullcontext()),
            (5, 6, 7, 8, nullcontext()),
            (9, 10, 11, 12, nullcontext()),
            (-1, 10, 11, 12, pytest.raises(ValueError)),
            (1, -1, 3, 4, pytest.raises(ValueError)),
            (1, 1, -3, 4, pytest.raises(ValueError)),
            (1, 1, 3, -4, pytest.raises(ValueError)),
            (-1, 1, 3, -4, pytest.raises(ValueError)),
            (-1, -1, 3, -4, pytest.raises(ValueError)),
            (-1, -1, -3, -4, pytest.raises(ValueError)),
            (1, -1, -3, -4, pytest.raises(ValueError)),
            (1, 1, -3, -4, pytest.raises(ValueError)),
        ],
    )
    def test_dimension_validate(self, width, height, weight, depth, expected):
        with expected:
            Dimension(width=width, height=height, weight=weight, depth=depth)

    @pytest.mark.parametrize(
        (
            "dimension__width",
            "dimension__height",
            "dimension__depth",
            "expected",
        ),
        [
            (1, 2, 3, 6),
            (5, 6, 7, 210),
            (9, 10, 11, 990),
        ],
    )
    def test_volume(self, dimension: Dimension, expected: float):
        assert dimension.volume == expected
