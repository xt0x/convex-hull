import pytest

from convex_hull.normalize import normalize_points
from convex_hull.types import Point


class _XY:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


def test_normalize_points_converts_pointlike_to_points_and_preserves_order() -> None:
    items = [_XY(2, 3), _XY(-1.5, 0.0), _XY(2, 3)]

    assert normalize_points(items) == [Point(2, 3), Point(-1.5, 0.0), Point(2, 3)]


def test_normalize_points_accepts_points_as_input() -> None:
    items = [Point(1, 2), Point(3, 4)]

    assert normalize_points(items) == [Point(1, 2), Point(3, 4)]


def test_normalize_points_accepts_generators() -> None:
    def gen():
        yield _XY(1, 1)
        yield _XY(2, 2)

    assert normalize_points(gen()) == [Point(1, 1), Point(2, 2)]


def test_normalize_points_raises_typeerror_when_missing_xy() -> None:
    class Bad:
        x = 1

    with pytest.raises(TypeError):
        normalize_points([Bad()])


def test_normalize_points_raises_typeerror_for_non_numeric_coordinates() -> None:
    with pytest.raises(TypeError):
        normalize_points([_XY("1", 2)])

    with pytest.raises(TypeError):
        normalize_points([_XY(1, object())])


def test_normalize_points_rejects_bool_coordinates() -> None:
    with pytest.raises(TypeError):
        normalize_points([_XY(True, 0)])
