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
- The package re-exports foundational types and constants from `__init__.py` to keep the public surface small.
- Future tasks will add geometry, normalization, and algorithm modules while keeping tests isolated under `tests/`.
