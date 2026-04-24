from dataclasses import dataclass

from convex_full import convex_hull
from convex_full.types import Point


@dataclass(frozen=True, slots=True)
class SamplePoint:
    x: int | float
    y: int | float


def test_convex_hull_square_returns_cyclic_order_with_lexicographic_start() -> None:
    points = [Point(1, 1), Point(0, 0), Point(1, 0), Point(0, 1)]

    assert convex_hull(points) == [
        Point(0, 0),
        Point(1, 0),
        Point(1, 1),
        Point(0, 1),
    ]


def test_convex_hull_removes_interior_points_for_concave_shape() -> None:
    points = [
        Point(0, 0),
        Point(3, 0),
        Point(3, 3),
        Point(2, 1),
        Point(0, 3),
        Point(1, 1),
    ]

    assert convex_hull(points) == [
        Point(0, 0),
        Point(3, 0),
        Point(3, 3),
        Point(0, 3),
    ]


def test_convex_hull_removes_edge_and_duplicate_points() -> None:
    points = [
        Point(0, 0),
        Point(2, 0),
        Point(4, 0),
        Point(4, 2),
        Point(4, 4),
        Point(2, 4),
        Point(0, 4),
        Point(0, 2),
        Point(0, 0),
        Point(2, 2),
    ]

    assert convex_hull(points) == [
        Point(0, 0),
        Point(4, 0),
        Point(4, 4),
        Point(0, 4),
    ]


def test_convex_hull_accepts_pointlike_inputs() -> None:
    points = [
        SamplePoint(0, 0),
        SamplePoint(2, 0),
        SamplePoint(1, 1),
        SamplePoint(0, 2),
    ]

    assert convex_hull(points) == [Point(0, 0), Point(2, 0), Point(0, 2)]


def test_convex_hull_handles_float_coordinates() -> None:
    points = [
        Point(0.0, 0.0),
        Point(2.5, 0.0),
        Point(1.0, 0.25),
        Point(2.5, 1.5),
        Point(0.0, 1.5),
    ]

    assert convex_hull(points) == [
        Point(0.0, 0.0),
        Point(2.5, 0.0),
        Point(2.5, 1.5),
        Point(0.0, 1.5),
    ]


def test_convex_hull_rotates_result_to_lexicographically_smallest_start() -> None:
    points = [
        Point(2, 2),
        Point(0, 2),
        Point(0, 0),
        Point(2, 0),
    ]

    hull = convex_hull(points)

    assert hull[0] == Point(0, 0)
    assert hull == [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
