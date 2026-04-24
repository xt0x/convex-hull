"""Polar transformation utilities (SPEC 4.3 / 5.6 first half).

This module converts points into polar representation around an interior pivot
point `P`, using `atan2` for the angle.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from convex_hull.geometry import is_zero_radius2
from convex_hull.types import PivotPoint, Point


@dataclass(frozen=True, slots=True)
class PolarItem:
    point: Point
    angle: float
    radius2: float


def sort_by_angle(items: list[PolarItem]) -> list[PolarItem]:
    """Return items sorted by ascending polar angle."""

    return sorted(items, key=lambda item: item.angle)


def same_direction(item1: PolarItem, item2: PolarItem, angle_epsilon: float) -> bool:
    """Return True if two items represent the same direction from the pivot.

    Uses a circular angle difference so 0 and 2π boundaries are treated as adjacent.
    """

    if angle_epsilon < 0:
        raise ValueError("angle_epsilon must be non-negative")

    two_pi = 2.0 * math.pi
    diff = abs(item1.angle - item2.angle)
    diff = min(diff, two_pi - diff)
    return diff <= angle_epsilon


def collapse_same_angle_keep_farthest(
    items: list[PolarItem], angle_epsilon: float
) -> list[PolarItem]:
    """Collapse same-direction items, keeping the farthest per direction.

    `items` must already be sorted by angle (use :func:`sort_by_angle`).

    Additionally merges the first and last items if they are in the same direction
    across the 0/2π boundary.
    """

    if angle_epsilon < 0:
        raise ValueError("angle_epsilon must be non-negative")

    if not items:
        return []

    collapsed: list[PolarItem] = []
    current = items[0]
    for item in items[1:]:
        if same_direction(current, item, angle_epsilon):
            if item.radius2 > current.radius2:
                # Keep the representative angle so the list stays sorted.
                current = PolarItem(
                    point=item.point, angle=current.angle, radius2=item.radius2
                )
            continue
        collapsed.append(current)
        current = item
    collapsed.append(current)

    if len(collapsed) >= 2 and same_direction(
        collapsed[0], collapsed[-1], angle_epsilon
    ):
        first = collapsed[0]
        last = collapsed[-1]
        if last.radius2 > first.radius2:
            merged = PolarItem(
                point=last.point, angle=first.angle, radius2=last.radius2
            )
        else:
            merged = first
        collapsed = [merged, *collapsed[1:-1]]

    return collapsed


def _normalize_angle(angle: float) -> float:
    # math.atan2 returns (-pi, pi]; normalize to [0, 2pi).
    two_pi = 2.0 * math.pi
    angle = angle % two_pi
    # Guard against -0.0 and the (rare) case where angle becomes exactly 2pi.
    if angle >= two_pi:
        angle -= two_pi
    return 0.0 if angle == 0.0 else angle


def build_polar_items(
    points: list[Point], pivot: PivotPoint, epsilon: float
) -> list[PolarItem]:
    """Build polar items for each point around the given `pivot`.

    Points with radius^2 effectively equal to 0 are excluded.
    """

    if epsilon < 0:
        raise ValueError("epsilon must be non-negative")

    items: list[PolarItem] = []
    for p in points:
        dx = float(p.x) - pivot.x
        dy = float(p.y) - pivot.y
        radius2 = dx * dx + dy * dy
        if is_zero_radius2(radius2, epsilon):
            continue
        angle = _normalize_angle(math.atan2(dy, dx))
        items.append(PolarItem(point=p, angle=angle, radius2=radius2))
    return items
