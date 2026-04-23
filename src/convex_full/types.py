"""Core type definitions for the convex hull domain."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, TypeAlias, runtime_checkable

Number: TypeAlias = int | float


@runtime_checkable
class PointLike(Protocol):
    """Public input contract for point-like values."""

    x: Number
    y: Number


@dataclass(frozen=True, slots=True)
class Point:
    """Normalized immutable point used in internal processing."""

    x: Number
    y: Number


@dataclass(frozen=True, slots=True)
class PivotPoint:
    """Interior pivot point represented with floating-point coordinates."""

    x: float
    y: float

