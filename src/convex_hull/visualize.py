"""Optional plotting helpers for visualizing points and their convex hull."""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any, TypeGuard

from convex_hull.algorithm import convex_hull
from convex_hull.types import Number, Point, PointLike
from convex_hull.validation import is_number_coordinate


def _is_number(value: object) -> TypeGuard[Number]:
    return is_number_coordinate(value)


def parse_point_collection(data: Any) -> list[Point]:
    """Parse a JSON-compatible point collection into internal points.

    Supported forms:
    - `[{"x": 0, "y": 1}, ...]`
    - `[[0, 1], [2, 3], ...]`
    """

    if not isinstance(data, list):
        raise TypeError("point collection must be a list")

    points: list[Point] = []
    for item in data:
        x: object
        y: object
        if isinstance(item, dict):
            if "x" not in item or "y" not in item:
                raise TypeError("point objects must contain x and y keys")
            x = item["x"]
            y = item["y"]
        elif isinstance(item, list | tuple):
            if len(item) != 2:
                raise TypeError("point arrays must contain exactly two values")
            x, y = item
        else:
            raise TypeError("each point must be an object with x/y or a 2-item array")

        if not _is_number(x) or not _is_number(y):
            raise TypeError("point coordinates must be int|float (bool is not allowed)")

        points.append(Point(x, y))

    return points


def load_points_from_json(path: str | Path) -> list[Point]:
    """Load points from a JSON file."""

    source = Path(path)
    try:
        raw = source.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise
    except OSError as exc:
        detail = exc.strerror or str(exc)
        raise OSError(f"failed to read {source}: {detail}") from exc

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON in {source}: line {exc.lineno} column {exc.colno}: {exc.msg}"
        ) from exc

    try:
        return parse_point_collection(data)
    except TypeError as exc:
        raise ValueError(f"invalid point collection in {source}: {exc}") from exc


def save_convex_hull_plot(
    points: Sequence[PointLike],
    output_path: str | Path,
    *,
    title: str = "Convex Hull",
    dpi: int = 150,
) -> Path:
    """Save a PNG visualization of points and their convex hull."""

    if dpi <= 0:
        raise ValueError("dpi must be a positive integer")

    try:
        import matplotlib
    except ModuleNotFoundError as exc:  # pragma: no cover
        raise RuntimeError(
            "Plotting requires matplotlib. Install with `uv sync --group dev` "
            "or `pip install .[plot]`."
        ) from exc

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    normalized_points = [Point(point.x, point.y) for point in points]
    hull = convex_hull(normalized_points)

    output = Path(output_path)
    fig = None
    try:
        output.parent.mkdir(parents=True, exist_ok=True)

        fig, ax = plt.subplots(figsize=(6, 6))

        point_x = [float(point.x) for point in normalized_points]
        point_y = [float(point.y) for point in normalized_points]
        ax.scatter(point_x, point_y, color="#1f77b4", label="points", zorder=2)

        if hull:
            hull_cycle = hull if len(hull) == 1 else [*hull, hull[0]]
            hull_x = [float(point.x) for point in hull_cycle]
            hull_y = [float(point.y) for point in hull_cycle]
            ax.plot(
                hull_x, hull_y, color="#d62728", linewidth=2, label="hull", zorder=3
            )
            ax.scatter(
                [float(point.x) for point in hull],
                [float(point.y) for point in hull],
                color="#d62728",
                s=45,
                zorder=4,
            )

        ax.set_title(title)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True, linestyle="--", alpha=0.3)
        ax.set_aspect("equal", adjustable="datalim")
        ax.legend(loc="best")

        fig.savefig(output, dpi=dpi, bbox_inches="tight")
    except OSError as exc:
        detail = exc.strerror or str(exc)
        raise OSError(f"failed to write plot to {output}: {detail}") from exc
    finally:
        if fig is not None:
            plt.close(fig)

    return output
