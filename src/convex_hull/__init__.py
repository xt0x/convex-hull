"""Top-level package for the convex hull library."""

from convex_hull._version import __version__
from convex_hull.algorithm import convex_hull
from convex_hull.constants import ANGLE_EPSILON, EPSILON
from convex_hull.types import Number, PivotPoint, Point, PointLike

__all__ = [
    "ANGLE_EPSILON",
    "EPSILON",
    "Number",
    "PivotPoint",
    "Point",
    "PointLike",
    "convex_hull",
    "__version__",
]
