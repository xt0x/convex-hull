"""Shared input validation helpers.

The project accepts integer and floating-point coordinates, but explicitly
rejects ``bool`` even though it is a subclass of ``int``.
"""

from __future__ import annotations

from typing import TypeGuard

from convex_hull.types import Number


def is_number_coordinate(value: object) -> TypeGuard[Number]:
    """Return True when `value` is a valid coordinate type."""

    return isinstance(value, (int, float)) and not isinstance(value, bool)
