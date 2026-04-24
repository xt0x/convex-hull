"""Prune non-extreme vertices from S' (SPEC 4.6, 4.7, 6.2-6.4)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, overload

from convex_hull.linked_list import CircularDoublyLinkedList, Node
from convex_hull.polar import PolarItem
from convex_hull.geometry import orient, orient_sign
from convex_hull.types import Point


@dataclass(frozen=True, slots=True)
class PruneStats:
    initial_n: int
    steps: int
    advances: int
    deletions: int


@overload
def prune_non_extreme_vertices(
    items: list[PolarItem], epsilon: float, *, return_stats: Literal[False] = False
) -> list[Point]: ...


@overload
def prune_non_extreme_vertices(
    items: list[PolarItem], epsilon: float, *, return_stats: Literal[True]
) -> tuple[list[Point], PruneStats]: ...


def prune_non_extreme_vertices(
    items: list[PolarItem], epsilon: float, *, return_stats: bool = False
) -> list[Point] | tuple[list[Point], PruneStats]:
    """Prune non-extreme vertices from a sorted, de-duplicated S' candidate list.

    The input `items` must represent S' in strictly increasing cyclic angle order.
    """

    if epsilon < 0:
        raise ValueError("epsilon must be non-negative")

    points = [item.point for item in items]
    ll = CircularDoublyLinkedList.from_items(points)
    initial_n = ll.size

    if ll.size <= 2:
        stats = PruneStats(initial_n=initial_n, steps=0, advances=0, deletions=0)
        result = list(ll)
        return (result, stats) if return_stats else result

    assert ll.head is not None
    middle: Node[Point] = ll.head
    validated_node_ids: set[int] = set()

    steps = 0
    advances = 0
    deletions = 0

    # Proof (SPEC 4.7) gives a < 2n' bound on steps. Keep a hard cap as a guard.
    max_steps = 2 * initial_n

    while ll.size > 2 and steps < max_steps:
        a = middle.prev
        b = middle
        c = middle.next

        turn = orient_sign(orient(a.item, b.item, c.item), epsilon)
        steps += 1

        if turn > 0:
            validated_node_ids.add(id(middle))
            middle = middle.next
            advances += 1
            if len(validated_node_ids) == ll.size:
                break
        else:
            to_delete = middle
            previous_node = middle.prev
            next_node = middle.next
            middle = middle.prev  # back up one point before deletion
            ll.delete(to_delete)
            deletions += 1
            validated_node_ids.discard(id(to_delete))
            validated_node_ids.discard(id(previous_node))
            validated_node_ids.discard(id(next_node))

        if ll.size <= 2:
            break

    if steps >= max_steps:
        raise RuntimeError("pruning did not terminate within the 2n' bound")

    stats = PruneStats(
        initial_n=initial_n, steps=steps, advances=advances, deletions=deletions
    )
    result = list(ll)
    return (result, stats) if return_stats else result
