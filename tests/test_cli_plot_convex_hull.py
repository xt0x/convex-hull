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


def test_cli_plot_convex_hull_reports_missing_input(
    tmp_path, monkeypatch, capsys
) -> None:
    output = tmp_path / "hull.png"

    monkeypatch.setattr(
        sys,
        "argv",
        ["convex-hull-plot", str(tmp_path / "missing.json"), str(output)],
    )

    assert main() == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "input file not found" in captured.err


def test_cli_plot_convex_hull_reports_invalid_json(
    tmp_path, monkeypatch, capsys
) -> None:
    source = tmp_path / "points.json"
    output = tmp_path / "hull.png"
    source.write_text("{not valid json}", encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        ["convex-hull-plot", str(source), str(output)],
    )

    assert main() == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "invalid JSON in" in captured.err
    assert "line 1 column 2" in captured.err


def test_cli_plot_convex_hull_rejects_non_positive_dpi(
    tmp_path, monkeypatch, capsys
) -> None:
    source = tmp_path / "points.json"
    output = tmp_path / "hull.png"
    source.write_text(json.dumps([[0, 0], [2, 0], [1, 1], [0, 2]]), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        ["convex-hull-plot", str(source), str(output), "--dpi", "0"],
    )

    assert main() == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "dpi must be a positive integer" in captured.err
