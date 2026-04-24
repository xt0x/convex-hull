"""Shared numeric tolerances for geometry operations.

`EPSILON` is a base relative tolerance. Geometry helpers derive scale-aware
thresholds from it instead of treating it as a fixed absolute cutoff.
"""

EPSILON = 1e-12
ANGLE_EPSILON = EPSILON
