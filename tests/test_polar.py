import math

import pytest

from convex_full.constants import EPSILON
from convex_full.polar import PolarItem, build_polar_items
from convex_full.types import PivotPoint, Point


def test_build_polar_items_computes_angles_and_radius2_and_preserves_order() -> None:
    pivot = PivotPoint(0.0, 0.0)
    points = [Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1)]

    items = build_polar_items(points, pivot, EPSILON)

    assert [i.point for i in items] == points
    assert [i.radius2 for i in items] == [1.0, 1.0, 1.0, 1.0]
    assert [i.angle for i in items] == pytest.approx(
        [0.0, math.pi / 2, math.pi, 3 * math.pi / 2]
    )


def test_build_polar_items_normalizes_angles_to_0_2pi() -> None:
    pivot = PivotPoint(0.0, 0.0)
    points = [Point(0, -1)]

    (item,) = build_polar_items(points, pivot, EPSILON)
    assert 0.0 <= item.angle < 2 * math.pi
    assert item.angle == pytest.approx(3 * math.pi / 2)


def test_build_polar_items_with_non_origin_pivot() -> None:
    pivot = PivotPoint(10.0, -2.0)
    points = [Point(11, -2), Point(10, -1)]

    items = build_polar_items(points, pivot, EPSILON)
    assert [i.radius2 for i in items] == [1.0, 1.0]
    assert [i.angle for i in items] == pytest.approx([0.0, math.pi / 2])


def test_build_polar_items_excludes_points_at_pivot() -> None:
    pivot = PivotPoint(0.0, 0.0)
    points = [Point(0, 0), Point(1, 0), Point(0, 0)]

    items = build_polar_items(points, pivot, EPSILON)
    assert [i.point for i in items] == [Point(1, 0)]


def test_build_polar_items_returns_polar_items() -> None:
    pivot = PivotPoint(0.0, 0.0)
    items = build_polar_items([Point(1, 0)], pivot, EPSILON)

    assert isinstance(items[0], PolarItem)


def test_build_polar_items_raises_for_invalid_epsilon() -> None:
    with pytest.raises(ValueError):
        build_polar_items([Point(1, 0)], PivotPoint(0.0, 0.0), -1.0)
