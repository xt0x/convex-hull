"""Geometry primitives used across the convex hull implementation."""

from __future__ import annotations

import math

from convex_hull.types import Number, PivotPoint, PointLike


def orient(a: PointLike, b: PointLike, c: PointLike) -> Number:
    """Return the signed area cross product for the turn a->b->c.

    Positive means counter-clockwise (left turn), negative clockwise, zero collinear.
    """

    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


def scaled_epsilon(epsilon: float, scale: float) -> float:
    """Return a scale-aware threshold derived from the base tolerance."""

    if epsilon < 0:
        raise ValueError("epsilon must be non-negative")

    magnitude = abs(scale)
    if magnitude == 0.0:
        magnitude = math.ulp(1.0)
    return epsilon * magnitude


def orient_sign(value: Number, epsilon: float, *, scale: float = 1.0) -> int:
    """Return -1/0/1 for value relative to a scale-aware tolerance."""

    threshold = scaled_epsilon(epsilon, scale)
    if value > threshold:
        return 1
    if value < -threshold:
        return -1
    return 0


def orientation_scale(a: PointLike, b: PointLike, c: PointLike) -> float:
    """Return a characteristic scale for the orientation predicate."""

    return (
        max(
            abs(float(b.x) - float(a.x)),
            abs(float(b.y) - float(a.y)),
            abs(float(c.x) - float(a.x)),
            abs(float(c.y) - float(a.y)),
        )
        ** 2
    )


def orient_turn_sign(a: PointLike, b: PointLike, c: PointLike, epsilon: float) -> int:
    """Return the orientation sign using a scale-aware threshold."""

    return orient_sign(orient(a, b, c), epsilon, scale=orientation_scale(a, b, c))


def squared_distance(a: PointLike, b: PointLike) -> Number:
    """Squared Euclidean distance between points."""

    dx = b.x - a.x
    dy = b.y - a.y
    return dx * dx + dy * dy


def centroid(a: PointLike, b: PointLike, c: PointLike) -> PivotPoint:
    """Centroid of a triangle defined by three points."""

    return PivotPoint((a.x + b.x + c.x) / 3.0, (a.y + b.y + c.y) / 3.0)


def is_zero_radius2(radius2: float, epsilon: float, *, scale: float = 1.0) -> bool:
    """Return True when the radius^2 value is effectively zero within tolerance."""

    return abs(radius2) <= scaled_epsilon(epsilon, scale)


def lexicographic_key(p: PointLike) -> tuple[Number, Number]:
    """Key function for lexicographic point ordering."""

    return (p.x, p.y)
