"""Input normalization.

The public API accepts "point-like" objects with ``x`` and ``y`` attributes.
This module converts those values into the internal immutable :class:`Point`.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import cast

from convex_hull.types import Number, Point, PointLike


def _is_number(value: object) -> bool:
    # `bool` is a subclass of `int`, but it's not a meaningful coordinate type here.
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def normalize_points(points: Iterable[PointLike]) -> list[Point]:
    """Convert `points` into a list of internal :class:`Point` values.

    - Preserves input order.
    - Does not remove duplicates. (Handled later in the pipeline.)
    """

    normalized: list[Point] = []
    for item in points:
        try:
            x = item.x
            y = item.y
        except AttributeError as exc:
            raise TypeError(
                f"PointLike must have x and y attributes; got {type(item).__name__}"
            ) from exc

        if not _is_number(x) or not _is_number(y):
            raise TypeError(
                "PointLike coordinates must be int|float (bool is not allowed); "
                f"got x={type(x).__name__}, y={type(y).__name__}"
            )

        normalized.append(Point(cast(Number, x), cast(Number, y)))

    return normalized
