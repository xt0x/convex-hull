import json

import pytest

from convex_full.types import Point
from convex_full.visualize import (
    load_points_from_json,
    parse_point_collection,
    save_convex_hull_plot,
)


def test_parse_point_collection_accepts_objects_and_arrays() -> None:
    assert parse_point_collection([{"x": 0, "y": 1}, [2, 3]]) == [
        Point(0, 1),
        Point(2, 3),
    ]


def test_parse_point_collection_rejects_invalid_shape() -> None:
    with pytest.raises(TypeError):
        parse_point_collection([{"x": 0}])


def test_load_points_from_json_reads_supported_format(tmp_path) -> None:
    source = tmp_path / "points.json"
    source.write_text(json.dumps([[0, 0], [2, 0], [0, 2]]), encoding="utf-8")

    assert load_points_from_json(source) == [Point(0, 0), Point(2, 0), Point(0, 2)]


def test_save_convex_hull_plot_writes_nonempty_png(tmp_path) -> None:
    output = tmp_path / "hull.png"

    saved = save_convex_hull_plot(
        [Point(0, 0), Point(2, 0), Point(1, 1), Point(0, 2)],
        output,
        title="Test Hull",
    )

    assert saved == output
    assert output.exists()
    assert output.suffix == ".png"
    assert output.stat().st_size > 0
