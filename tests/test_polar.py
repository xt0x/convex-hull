import math

import pytest

from convex_full.constants import ANGLE_EPSILON, EPSILON
from convex_full.polar import (
    PolarItem,
    build_polar_items,
    collapse_same_angle_keep_farthest,
    same_direction,
    sort_by_angle,
)
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


def test_sort_by_angle_sorts_ascending() -> None:
    items = [
        PolarItem(Point(0, 0), angle=2.0, radius2=1.0),
        PolarItem(Point(0, 0), angle=0.5, radius2=1.0),
        PolarItem(Point(0, 0), angle=1.0, radius2=1.0),
    ]

    assert [i.angle for i in sort_by_angle(items)] == [0.5, 1.0, 2.0]


def test_same_direction_wraps_around_zero_and_2pi() -> None:
    two_pi = 2.0 * math.pi
    a = PolarItem(Point(1, 0), angle=0.0001, radius2=1.0)
    b = PolarItem(Point(2, 0), angle=two_pi - 0.00005, radius2=4.0)

    assert same_direction(a, b, angle_epsilon=0.001)


def test_collapse_same_angle_keep_farthest_keeps_farthest_in_group() -> None:
    items = [
        PolarItem(Point(1, 0), angle=0.1, radius2=1.0),
        PolarItem(Point(2, 0), angle=0.1 + ANGLE_EPSILON * 0.5, radius2=4.0),
        PolarItem(Point(0, 1), angle=1.0, radius2=1.0),
    ]

    collapsed = collapse_same_angle_keep_farthest(sort_by_angle(items), ANGLE_EPSILON)
    assert [i.point for i in collapsed] == [Point(2, 0), Point(0, 1)]


def test_collapse_same_angle_keep_farthest_merges_first_and_last_across_boundary() -> (
    None
):
    two_pi = 2.0 * math.pi
    items = [
        PolarItem(Point(1, 0), angle=0.01, radius2=1.0),
        PolarItem(Point(0, 1), angle=1.0, radius2=1.0),
        PolarItem(Point(2, 0), angle=two_pi - 0.005, radius2=4.0),
    ]

    collapsed = collapse_same_angle_keep_farthest(
        sort_by_angle(items), angle_epsilon=0.02
    )

    assert len(collapsed) == 2
    assert collapsed[0].point == Point(2, 0)
    assert collapsed[0].radius2 == 4.0
    assert collapsed[0].angle == pytest.approx(0.01)
    assert collapsed[1].point == Point(0, 1)
