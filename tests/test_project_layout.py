from importlib import import_module
from pathlib import Path
import tomllib


def test_runtime_dependencies_are_empty() -> None:
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))

    assert data["project"]["dependencies"] == []


def test_src_layout_package_is_importable() -> None:
    module = import_module("convex_full")

    assert hasattr(module, "__all__")


def test_tests_directory_exists() -> None:
    tests_dir = Path(__file__).resolve().parent

    assert tests_dir.exists()
    assert tests_dir.is_dir()
