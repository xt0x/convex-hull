import json
import sys

from convex_hull.cli.plot_convex_hull import main


def test_cli_plot_convex_hull_writes_png(tmp_path, monkeypatch, capsys) -> None:
    source = tmp_path / "points.json"
    output = tmp_path / "hull.png"
    source.write_text(json.dumps([[0, 0], [2, 0], [1, 1], [0, 2]]), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "convex-hull-plot",
            str(source),
            str(output),
            "--title",
            "CLI Test",
        ],
    )

    assert main() == 0
    assert output.exists()
    assert output.stat().st_size > 0
    assert "saved plot to" in capsys.readouterr().out
