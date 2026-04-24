from dataclasses import FrozenInstanceError

import pytest

from convex_hull.constants import ANGLE_EPSILON, EPSILON
from convex_hull.types import PivotPoint, Point


def test_point_value_equality_and_hashability() -> None:
    point_a = Point(1, 2)
    point_b = Point(1, 2)

    assert point_a == point_b
    assert hash(point_a) == hash(point_b)
    assert {point_a, point_b} == {Point(1, 2)}


def test_point_is_immutable() -> None:
    point = Point(1, 2)

    with pytest.raises(FrozenInstanceError):
        point.x = 3


def test_point_sorting_is_stable_with_lexicographic_key() -> None:
    points = [Point(3, 0), Point(1, 5), Point(1, 2), Point(-1, 7)]

    assert sorted(points, key=lambda point: (point.x, point.y)) == [
        Point(-1, 7),
        Point(1, 2),
        Point(1, 5),
        Point(3, 0),
    ]


def test_pivot_point_stores_float_coordinates() -> None:
    pivot = PivotPoint(1.5, -2.0)

    assert pivot.x == 1.5
    assert pivot.y == -2.0
    assert isinstance(pivot.x, float)
    assert isinstance(pivot.y, float)


def test_angle_epsilon_defaults_to_epsilon() -> None:
    assert ANGLE_EPSILON == EPSILON
    assert EPSILON > 0
