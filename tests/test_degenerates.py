import pytest

from convex_full.constants import EPSILON
from convex_full.degenerates import (
    all_collinear,
    handle_degenerate_cases,
    remove_exact_duplicates,
    two_endpoints_of_collinear_set,
)
from convex_full.types import Point


def test_remove_exact_duplicates_preserves_order() -> None:
    points = [Point(0, 0), Point(1, 1), Point(0, 0), Point(2, 2), Point(1, 1)]

    assert remove_exact_duplicates(points) == [Point(0, 0), Point(1, 1), Point(2, 2)]


def test_all_collinear_true_for_small_inputs() -> None:
    assert all_collinear([], EPSILON)
    assert all_collinear([Point(0, 0)], EPSILON)
    assert all_collinear([Point(0, 0), Point(1, 1)], EPSILON)


def test_all_collinear_vertical_line() -> None:
    points = [Point(2, -1), Point(2, 0), Point(2, 100)]
    assert all_collinear(points, EPSILON)


def test_all_collinear_false_for_triangle() -> None:
    points = [Point(0, 0), Point(1, 0), Point(0, 1)]
    assert not all_collinear(points, EPSILON)


def test_two_endpoints_of_collinear_set_vertical_line() -> None:
    points = [Point(2, -1), Point(2, 0), Point(2, 100)]

    assert two_endpoints_of_collinear_set(points) == [Point(2, -1), Point(2, 100)]


def test_two_endpoints_of_collinear_set_slanted_line() -> None:
    points = [Point(-1, -1), Point(0, 0), Point(2, 2), Point(1, 1)]

    assert two_endpoints_of_collinear_set(points) == [Point(-1, -1), Point(2, 2)]


def test_handle_degenerate_cases_empty_and_singleton() -> None:
    assert handle_degenerate_cases([], EPSILON) == []
    assert handle_degenerate_cases([Point(1, 2)], EPSILON) == [Point(1, 2)]


def test_handle_degenerate_cases_two_points_with_duplicates() -> None:
    points = [Point(0, 0), Point(0, 0), Point(1, 1)]

    assert handle_degenerate_cases(points, EPSILON) == [Point(0, 0), Point(1, 1)]


def test_handle_degenerate_cases_all_duplicates() -> None:
    points = [Point(1, 1), Point(1, 1), Point(1, 1)]

    assert handle_degenerate_cases(points, EPSILON) == [Point(1, 1)]


def test_handle_degenerate_cases_all_collinear_returns_endpoints_only() -> None:
    points = [Point(0, 0), Point(2, 2), Point(1, 1), Point(-1, -1), Point(0, 0)]

    assert handle_degenerate_cases(points, EPSILON) == [Point(-1, -1), Point(2, 2)]


def test_handle_degenerate_cases_non_degenerate_returns_none() -> None:
    points = [Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1)]

    assert handle_degenerate_cases(points, EPSILON) is None


def test_handle_degenerate_cases_raises_for_invalid_epsilon() -> None:
    with pytest.raises(ValueError):
        handle_degenerate_cases([Point(0, 0)], -1.0)
