"""Public convex hull API (SPEC 5.2 / chapter 7)."""

from __future__ import annotations

from collections.abc import Iterable

from convex_hull.constants import ANGLE_EPSILON, EPSILON
from convex_hull.degenerates import handle_degenerate_cases, remove_exact_duplicates
from convex_hull.geometry import lexicographic_key
from convex_hull.normalize import normalize_points
from convex_hull.pivot import compute_interior_point
from convex_hull.polar import (
    PolarItem,
    build_polar_items,
    collapse_same_angle_keep_farthest,
    sort_by_angle,
)
from convex_hull.prune import prune_non_extreme_vertices
from convex_hull.types import Point, PointLike


def rotate_to_lexicographically_smallest_start(points: list[Point]) -> list[Point]:
    """Rotate a cyclic point list so the lexicographically smallest point is first."""

    if len(points) <= 1:
        return list(points)

    start = min(range(len(points)), key=lambda index: lexicographic_key(points[index]))
    return [*points[start:], *points[:start]]


def points_from(items: list[PolarItem]) -> list[Point]:
    """Project polar items back to their points."""

    return [item.point for item in items]


def convex_hull(points: Iterable[PointLike]) -> list[Point]:
    """Compute the convex hull in cyclic order.

    The returned sequence is normalized so the lexicographically smallest point
    is always first.
    """

    normalized = normalize_points(points)
    unique = remove_exact_duplicates(normalized)

    degenerate = handle_degenerate_cases(unique, EPSILON)
    if degenerate is not None:
        return rotate_to_lexicographically_smallest_start(degenerate)

    pivot = compute_interior_point(unique, EPSILON)
    if pivot is None:
        return rotate_to_lexicographically_smallest_start(unique)

    items = build_polar_items(unique, pivot, EPSILON)
    items = sort_by_angle(items)
    items = collapse_same_angle_keep_farthest(items, ANGLE_EPSILON)

    if len(items) <= 2:
        return rotate_to_lexicographically_smallest_start(points_from(items))

    hull = prune_non_extreme_vertices(items, EPSILON)
    return rotate_to_lexicographically_smallest_start(hull)
