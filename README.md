# convex-full

Minimal `uv`-managed library scaffold for the convex hull implementation plan in [docs/SPEC.md](docs/SPEC.md).

## Development

- Install and sync dependencies with `uv sync`
- Run tests with `uv run pytest`

## Visualization

- Add points to a JSON file as either `[{"x": 0, "y": 0}, ...]` or `[[0, 0], ...]`
- Render a PNG with `uv run convex-full-plot points.json output/hull.png`
- Module form is also available: `uv run python -m convex_full.cli.plot_convex_hull points.json output/hull.png`
- Optional title/dpi example: `uv run convex-full-plot points.json output/hull.png --title "Sample Hull" --dpi 200`

Example `points.json`:

```json
[
  {"x": 0, "y": 0},
  {"x": 2, "y": 0},
  {"x": 1, "y": 1},
  {"x": 2, "y": 2},
  {"x": 0, "y": 2}
]
```

## Project layout

- `src/convex_full/`: library package
- `src/convex_full/cli/`: Python CLI entry points for developer utilities
- `tests/`: automated tests
- `docs/`: specification and implementation plan
