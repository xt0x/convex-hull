"""Interior point selection (SPEC 4.2 / 5.5).

We find the first non-collinear triple in the (already de-duplicated) input and
use its centroid as an interior reference point `P`.
"""

from __future__ import annotations

from collections.abc import Sequence

from convex_hull.geometry import centroid, lexicographic_key, orient_turn_sign
from convex_hull.types import PivotPoint, Point


def find_first_non_collinear_triple(
    points: Sequence[Point], epsilon: float
) -> tuple[Point, Point, Point] | None:
    """Return the first non-collinear triple, or None if not found.

    The scan is linear. For a collinear triple (a, b, c), we drop the "middle"
    point by updating (a, b) to the lexicographic endpoints among {a, b, c}.
    """

    if epsilon < 0:
        raise ValueError("epsilon must be non-negative")

    if len(points) < 3:
        return None

    a = points[0]
    b = points[1]

    # In normal flow duplicates are removed earlier, but be defensive here.
    idx = 2
    while a == b and idx < len(points):
        b = points[idx]
        idx += 1

    if a == b:
        return None

    for c in points[idx:]:
        if c == a or c == b:
            continue

        if orient_turn_sign(a, b, c, epsilon) != 0:
            return (a, b, c)

        # Still collinear; keep endpoints for a stable baseline.
        low = min((a, b, c), key=lexicographic_key)
        high = max((a, b, c), key=lexicographic_key)
        a, b = low, high

        if a == b:
            return None

    return None


def compute_interior_point(
    points: Sequence[Point], epsilon: float
) -> PivotPoint | None:
    """Compute the interior point P as the centroid of the first non-collinear triple."""

    triple = find_first_non_collinear_triple(points, epsilon)
    if triple is None:
        return None
    a, b, c = triple
    return centroid(a, b, c)
