"""Geometry primitives used across the convex hull implementation."""

from __future__ import annotations

from convex_hull.types import Number, PivotPoint, PointLike


def orient(a: PointLike, b: PointLike, c: PointLike) -> float:
    """Return the signed area cross product for the turn a->b->c.

    Positive means counter-clockwise (left turn), negative clockwise, zero collinear.
    """

    return float((b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x))


def orient_sign(value: float, epsilon: float) -> int:
    """Return -1/0/1 for value relative to the given tolerance."""

    if value > epsilon:
        return 1
    if value < -epsilon:
        return -1
    return 0


def squared_distance(a: PointLike, b: PointLike) -> float:
    """Squared Euclidean distance between points."""

    dx = b.x - a.x
    dy = b.y - a.y
    return float(dx * dx + dy * dy)


def centroid(a: PointLike, b: PointLike, c: PointLike) -> PivotPoint:
    """Centroid of a triangle defined by three points."""

    return PivotPoint((a.x + b.x + c.x) / 3.0, (a.y + b.y + c.y) / 3.0)


def is_zero_radius2(radius2: float, epsilon: float) -> bool:
    """Return True when the radius^2 value is effectively zero within tolerance."""

    return abs(radius2) <= epsilon


def lexicographic_key(p: PointLike) -> tuple[Number, Number]:
    """Key function for lexicographic point ordering."""

    return (p.x, p.y)
