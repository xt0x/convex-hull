# Source Design

`src/` contains the application library code only.

- `convex_full/` is the root package for the convex hull implementation.
- The package currently exposes a minimal public version constant and acts as the T0 scaffold.
- Future tasks will add geometry, normalization, and algorithm modules while keeping tests isolated under `tests/`.
