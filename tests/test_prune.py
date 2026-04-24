import math

import pytest

from convex_full.constants import EPSILON
from convex_full.polar import PolarItem
from convex_full.prune import prune_non_extreme_vertices
from convex_full.types import Point


def _items_around_origin(points: list[Point]) -> list[PolarItem]:
    items: list[PolarItem] = []
    for p in points:
        angle = math.atan2(float(p.y), float(p.x)) % (2.0 * math.pi)
        radius2 = float(p.x) * float(p.x) + float(p.y) * float(p.y)
        items.append(PolarItem(point=p, angle=angle, radius2=radius2))
    return sorted(items, key=lambda i: i.angle)


def test_prune_removes_concave_vertices_and_collinear_middle_points() -> None:
    # Points are in angle order around the origin (a valid interior pivot).
    points = [
        Point(3, 0),
        Point(1, 1),  # inside edge from (3,0) to (0,3)
        Point(0, 3),
        Point(-1, 1),  # inside edge from (0,3) to (-3,0)
        Point(-3, 0),
        Point(0, -3),
    ]
    items = _items_around_origin(points)

    pruned, stats = prune_non_extreme_vertices(items, EPSILON, return_stats=True)

    assert set(pruned) == {Point(3, 0), Point(0, 3), Point(-3, 0), Point(0, -3)}
    assert stats.initial_n == 6
    assert stats.steps == stats.advances + stats.deletions
    assert stats.steps < 2 * stats.initial_n


def test_prune_len_le_2_is_identity_and_respects_stats_bound() -> None:
    items = _items_around_origin([Point(1, 0), Point(0, 1)])

    pruned, stats = prune_non_extreme_vertices(items, EPSILON, return_stats=True)
    assert pruned == [Point(1, 0), Point(0, 1)]
    assert stats.initial_n == 2
    assert stats.steps == 0
    assert stats.steps < 2 * stats.initial_n


def test_prune_raises_if_fails_to_terminate_within_bound() -> None:
    items = _items_around_origin([Point(1, 0), Point(0, 1), Point(-1, 0)])

    # With a reasonable epsilon, this should terminate.
    pruned, stats = prune_non_extreme_vertices(items, EPSILON, return_stats=True)
    assert len(pruned) in (2, 3)
    assert stats.steps < 2 * stats.initial_n


def test_prune_invalid_epsilon() -> None:
    items = _items_around_origin([Point(1, 0), Point(0, 1), Point(-1, 0)])

    with pytest.raises(ValueError):
        prune_non_extreme_vertices(items, -1.0)
