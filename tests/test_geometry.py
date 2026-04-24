import math

import pytest

from convex_hull.constants import EPSILON
from convex_hull.geometry import (
    centroid,
    is_zero_radius2,
    lexicographic_key,
    orient,
    orient_sign,
    squared_distance,
)
from convex_hull.types import PivotPoint, Point


def test_orient_left_turn_right_turn_and_collinear() -> None:
    a = Point(0, 0)
    b = Point(1, 0)

    assert orient(a, b, Point(1, 1)) > 0
    assert orient(a, b, Point(1, -1)) < 0
    assert orient(a, b, Point(2, 0)) == 0


def test_orient_with_negative_coordinates() -> None:
    a = Point(-1, -1)
    b = Point(2, -1)
    c = Point(0, 3)

    assert orient(a, b, c) > 0


@pytest.mark.parametrize(
    ("value", "epsilon", "expected"),
    [
        (1.0, 0.1, 1),
        (0.05, 0.1, 0),
        (-0.05, 0.1, 0),
        (-1.0, 0.1, -1),
    ],
)
def test_orient_sign(value: float, epsilon: float, expected: int) -> None:
    assert orient_sign(value, epsilon) == expected


def test_squared_distance() -> None:
    assert squared_distance(Point(0, 0), Point(3, 4)) == 25.0
    assert squared_distance(Point(-1, -1), Point(2, 3)) == 25.0


def test_centroid_returns_pivot_point() -> None:
    pivot = centroid(Point(0, 0), Point(3, 0), Point(0, 3))

    assert isinstance(pivot, PivotPoint)
    assert math.isclose(pivot.x, 1.0)
    assert math.isclose(pivot.y, 1.0)


def test_is_zero_radius2() -> None:
    assert is_zero_radius2(0.0, EPSILON)
    assert is_zero_radius2(EPSILON * 0.5, EPSILON)
    assert is_zero_radius2(-EPSILON * 0.5, EPSILON)
    assert not is_zero_radius2(EPSILON * 2, EPSILON)


def test_lexicographic_key() -> None:
    assert lexicographic_key(Point(1, 2)) == (1, 2)
