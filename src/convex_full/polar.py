"""Polar transformation utilities (SPEC 4.3 / 5.6 first half).

This module converts points into polar representation around an interior pivot
point `P`, using `atan2` for the angle.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from convex_full.geometry import is_zero_radius2
from convex_full.types import PivotPoint, Point


@dataclass(frozen=True, slots=True)
class PolarItem:
    point: Point
    angle: float
    radius2: float


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
