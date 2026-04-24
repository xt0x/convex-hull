import random

from convex_full import convex_hull
from convex_full.constants import ANGLE_EPSILON, EPSILON
from convex_full.degenerates import remove_exact_duplicates
from convex_full.normalize import normalize_points
from convex_full.pivot import compute_interior_point
from convex_full.polar import (
    build_polar_items,
    collapse_same_angle_keep_farthest,
    sort_by_angle,
)
from convex_full.prune import prune_non_extreme_vertices
from convex_full.types import Point


def _cross(origin: Point, a: Point, b: Point) -> float:
    return float(
        (a.x - origin.x) * (b.y - origin.y) - (a.y - origin.y) * (b.x - origin.x)
    )


def _monotonic_chain(points: list[Point]) -> list[Point]:
    unique = sorted(remove_exact_duplicates(points), key=lambda p: (p.x, p.y))
    if len(unique) <= 1:
        return unique

    lower: list[Point] = []
    for point in unique:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)

    upper: list[Point] = []
    for point in reversed(unique):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)

    hull = lower[:-1] + upper[:-1]
    if not hull:
        return []

    start = min(range(len(hull)), key=lambda index: (hull[index].x, hull[index].y))
    return [*hull[start:], *hull[:start]]


def _build_s_prime(points: list[Point]):
    normalized = remove_exact_duplicates(normalize_points(points))
    pivot = compute_interior_point(normalized, EPSILON)
    assert pivot is not None
    items = build_polar_items(normalized, pivot, EPSILON)
    items = sort_by_angle(items)
    return collapse_same_angle_keep_farthest(items, ANGLE_EPSILON)


def test_acceptance_8_1_1_output_extreme_points_match_expected() -> None:
    points = [
        Point(0, 0),
        Point(4, 0),
        Point(4, 4),
        Point(2, 2),
        Point(0, 4),
        Point(1, 3),
    ]

    assert convex_hull(points) == [
        Point(0, 0),
        Point(4, 0),
        Point(4, 4),
        Point(0, 4),
    ]


def test_acceptance_8_1_2_same_angle_keeps_only_farthest_point() -> None:
    points = [Point(-2, 0), Point(2, 0), Point(0, 3), Point(0, 2)]

    assert convex_hull(points) == [Point(-2, 0), Point(2, 0), Point(0, 3)]


def test_acceptance_8_1_3_step_5_deletes_non_extreme_points() -> None:
    points = [
        Point(3, 0),
        Point(1, 1),
        Point(0, 3),
        Point(-1, 1),
        Point(-3, 0),
        Point(0, -3),
    ]

    pruned, stats = prune_non_extreme_vertices(
        _build_s_prime(points), EPSILON, return_stats=True
    )

    assert stats.deletions > 0
    assert set(pruned) == {Point(3, 0), Point(0, 3), Point(-3, 0), Point(0, -3)}


def test_acceptance_8_1_4_prune_leaves_only_extreme_points() -> None:
    points = [
        Point(0, 0),
        Point(-2, 2),
        Point(-3, -3),
        Point(2, -2),
        Point(0, -1),
    ]

    pruned, _stats = prune_non_extreme_vertices(
        _build_s_prime(points), EPSILON, return_stats=True
    )

    assert pruned == [Point(-2, 2), Point(-3, -3), Point(2, -2)]


def test_acceptance_8_2_1_duplicates_do_not_change_result() -> None:
    base = [Point(0, 0), Point(3, 0), Point(3, 3), Point(0, 3), Point(1, 1)]
    duplicated = base + [Point(0, 0), Point(3, 0), Point(1, 1), Point(3, 3)]

    assert convex_hull(duplicated) == convex_hull(base)


def test_acceptance_8_2_2_all_collinear_returns_only_endpoints() -> None:
    points = [Point(2, 2), Point(-1, -1), Point(0, 0), Point(3, 3), Point(1, 1)]

    assert convex_hull(points) == [Point(-1, -1), Point(3, 3)]


def test_acceptance_8_2_3_edge_midpoints_are_not_returned() -> None:
    points = [
        Point(0, 0),
        Point(2, 0),
        Point(4, 0),
        Point(4, 2),
        Point(4, 4),
        Point(2, 4),
        Point(0, 4),
        Point(0, 2),
    ]

    assert convex_hull(points) == [
        Point(0, 0),
        Point(4, 0),
        Point(4, 4),
        Point(0, 4),
    ]


def test_acceptance_8_2_4_integer_and_float_inputs_are_both_supported() -> None:
    int_points = [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2), Point(1, 1)]
    float_points = [
        Point(0.0, 0.0),
        Point(2.0, 0.0),
        Point(2.0, 2.0),
        Point(0.0, 2.0),
        Point(1.0, 1.0),
    ]

    assert convex_hull(int_points) == [
        Point(0, 0),
        Point(2, 0),
        Point(2, 2),
        Point(0, 2),
    ]
    assert convex_hull(float_points) == [
        Point(0.0, 0.0),
        Point(2.0, 0.0),
        Point(2.0, 2.0),
        Point(0.0, 2.0),
    ]


def test_acceptance_8_2_5_matches_monotonic_chain_reference() -> None:
    random.seed(7)

    for size in range(1, 16):
        for _ in range(20):
            points = [
                Point(random.randint(-4, 4), random.randint(-4, 4)) for _ in range(size)
            ]
            assert set(convex_hull(points)) == set(_monotonic_chain(points))


def test_termination_stats_stay_under_2n_prime_on_representative_inputs() -> None:
    cases = [
        [
            Point(3, 0),
            Point(1, 1),
            Point(0, 3),
            Point(-1, 1),
            Point(-3, 0),
            Point(0, -3),
        ],
        [Point(0, 0), Point(-2, 2), Point(-3, -3), Point(2, -2), Point(0, -1)],
        [Point(-2, 0), Point(2, 0), Point(0, 3), Point(0, 2), Point(-1, 1)],
    ]

    for points in cases:
        _pruned, stats = prune_non_extreme_vertices(
            _build_s_prime(points), EPSILON, return_stats=True
        )
        assert stats.steps == stats.advances + stats.deletions
        assert stats.steps < 2 * stats.initial_n
        assert stats.advances >= 0
        assert stats.deletions >= 0
