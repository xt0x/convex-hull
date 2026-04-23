"""Top-level package for the convex hull library."""

from convex_full.constants import ANGLE_EPSILON, EPSILON
from convex_full.types import Number, PivotPoint, Point, PointLike

__all__ = [
    "ANGLE_EPSILON",
    "EPSILON",
    "Number",
    "PivotPoint",
    "Point",
    "PointLike",
    "__version__",
]

__version__ = "0.1.0"
