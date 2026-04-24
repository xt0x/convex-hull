from convex_hull.constants import EPSILON
from convex_hull.pivot import compute_interior_point, find_first_non_collinear_triple
from convex_hull.types import PivotPoint, Point


def test_find_first_non_collinear_triple_found_immediately() -> None:
    points = [Point(0, 0), Point(1, 0), Point(0, 1), Point(10, 10)]

    triple = find_first_non_collinear_triple(points, EPSILON)
    assert triple == (Point(0, 0), Point(1, 0), Point(0, 1))


def test_find_first_non_collinear_triple_after_long_collinear_prefix() -> None:
    # Many points on y=0, then a point off the line.
    points = [
        Point(0, 0),
        Point(1, 0),
        Point(2, 0),
        Point(3, 0),
        Point(4, 0),
        Point(2, 2),
    ]

    triple = find_first_non_collinear_triple(points, EPSILON)
    assert triple is not None
    a, b, c = triple
    assert c == Point(2, 2)
    assert a.y == 0 and b.y == 0


def test_find_first_non_collinear_triple_none_when_all_collinear() -> None:
    points = [Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3)]

    assert find_first_non_collinear_triple(points, EPSILON) is None


def test_compute_interior_point_returns_centroid() -> None:
    points = [Point(0, 0), Point(3, 0), Point(0, 3)]

    pivot = compute_interior_point(points, EPSILON)
    assert isinstance(pivot, PivotPoint)
    assert pivot == PivotPoint(1.0, 1.0)


def test_compute_interior_point_none_when_all_collinear() -> None:
    points = [Point(0, 0), Point(1, 0), Point(2, 0)]

    assert compute_interior_point(points, EPSILON) is None
