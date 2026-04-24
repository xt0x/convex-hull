# Source Design

`src/` contains the application library code only.

- `convex_full/` is the root package for the convex hull implementation.
- `types.py` defines the public point contract and immutable internal point models.
- `constants.py` centralizes numeric tolerances so later geometry modules share one source of truth.
- `normalize.py` converts public PointLike inputs into internal `Point` values while preserving order.
- `geometry.py` provides pure geometry helpers (orientation, distances, centroid, lexicographic ordering).
- `linked_list.py` provides a doubly-linked circular list for the prune step's delete-and-rewind behavior.
- `degenerates.py` removes exact duplicates and handles degenerate inputs (empty, 1/2 points, all-collinear).
- `pivot.py` finds a non-collinear triple and computes an interior reference point `P` (triangle centroid).
- `polar.py` converts points into polar form around `P` (angle via `atan2` and radius^2), and provides utilities for sorting by angle and collapsing same-direction points into `S'`.
- `prune.py` performs the step-5 deletion iteration on `S'` using a circular list, and can return termination statistics.
- `algorithm.py` wires the full pipeline into the public `convex_hull(points)` API and normalizes the output start point.
- `visualize.py` provides optional developer-side helpers for loading JSON points and rendering a PNG via `matplotlib`.
- `cli/` contains command-line entry points layered on top of the library so future developer tools can grow without mixing with shell scripts.
- The package re-exports foundational types and constants from `__init__.py` to keep the public surface small.
- Tests stay isolated under `tests/`, including unit coverage for each helper stage and integration coverage for the public API.
