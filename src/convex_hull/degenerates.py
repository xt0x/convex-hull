"""Duplicate removal and degenerate-input handling (SPEC 5.3, 5.4)."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

from convex_hull.geometry import lexicographic_key, orient_turn_sign
from convex_hull.types import Point


def remove_exact_duplicates(points: Iterable[Point]) -> list[Point]:
    """Remove exactly-equal duplicate points while preserving input order."""

    seen: set[Point] = set()
    unique: list[Point] = []
    for p in points:
        if p in seen:
            continue
        seen.add(p)
        unique.append(p)
    return unique


def all_collinear(points: Sequence[Point], epsilon: float) -> bool:
    """Return True if all points are collinear within tolerance."""

    if epsilon < 0:
        raise ValueError("epsilon must be non-negative")

    if len(points) <= 2:
        return True

    # Find a non-degenerate baseline (a != b).
    a = points[0]
    b = None
    for candidate in points[1:]:
        if candidate != a:
            b = candidate
            break
    if b is None:
        return True

    for c in points:
        if orient_turn_sign(a, b, c, epsilon) != 0:
            return False
    return True


def two_endpoints_of_collinear_set(points: Sequence[Point]) -> list[Point]:
    """Return the two lexicographic endpoints of a (possibly duplicate) collinear set."""

    if not points:
        return []

    low = min(points, key=lexicographic_key)
    high = max(points, key=lexicographic_key)
    if low == high:
        return [low]
    return [low, high]


def prepare_points(
    points: Sequence[Point], epsilon: float
) -> tuple[list[Point], list[Point] | None]:
    """Return `(unique_points, degenerate_hull_or_none)` for the input.

    This is a small helper for wiring the pipeline without repeating the
    de-duplication work in callers.
    """

    if epsilon < 0:
        raise ValueError("epsilon must be non-negative")

    unique = remove_exact_duplicates(points)

    if len(unique) == 0:
        return (unique, [])
    if len(unique) == 1:
        return (unique, [unique[0]])
    if len(unique) == 2:
        return (unique, unique)

    if all_collinear(unique, epsilon):
        return (unique, two_endpoints_of_collinear_set(unique))

    return (unique, None)


def handle_degenerate_cases(
    points: Sequence[Point], epsilon: float
) -> list[Point] | None:
    """Handle degenerate inputs.

    Returns:
        - A hull result (possibly empty) for degenerate inputs.
        - None for the normal case (>= 3 non-collinear points) so the algorithm can proceed.
    """

    if epsilon < 0:
        raise ValueError("epsilon must be non-negative")

    _unique, degenerate = prepare_points(points, epsilon)
    return degenerate
