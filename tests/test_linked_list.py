from __future__ import annotations

import pytest

from convex_full.linked_list import CircularDoublyLinkedList, Node


def _collect_items_from(node: Node[int]) -> list[int]:
    return [n.item for n in node.iter_cycle()]


def test_from_items_empty() -> None:
    ll = CircularDoublyLinkedList.from_items([])

    assert ll.head is None
    assert ll.size == 0
    assert list(ll) == []


def test_from_items_size_1_invariants() -> None:
    ll = CircularDoublyLinkedList.from_items([10])
    assert ll.size == 1
    assert ll.head is not None

    head = ll.head
    assert head.next is head
    assert head.prev is head
    assert head.next.prev is head
    assert head.prev.next is head
    assert list(ll) == [10]


def test_from_items_size_3_and_iter_cycle_from_any_node() -> None:
    ll = CircularDoublyLinkedList.from_items([1, 2, 3])
    assert ll.size == 3
    assert list(ll) == [1, 2, 3]

    assert ll.head is not None
    n1 = ll.head
    n2 = n1.next
    n3 = n2.next

    assert _collect_items_from(n1) == [1, 2, 3]
    assert _collect_items_from(n2) == [2, 3, 1]
    assert _collect_items_from(n3) == [3, 1, 2]


def test_delete_middle_node_keeps_invariants() -> None:
    ll = CircularDoublyLinkedList.from_items([1, 2, 3, 4])
    assert ll.head is not None

    node_2 = ll.head.next
    ll.delete(node_2)

    assert ll.size == 3
    assert list(ll) == [1, 3, 4]

    head = ll.head
    assert head is not None
    for node in head.iter_cycle():
        assert node.next.prev is node
        assert node.prev.next is node


def test_delete_head_updates_representative_node() -> None:
    ll = CircularDoublyLinkedList.from_items([1, 2, 3])
    assert ll.head is not None
    old_head = ll.head

    ll.delete(old_head)

    assert ll.size == 2
    assert ll.head is not None
    assert ll.head.item == 2
    assert list(ll) == [2, 3]


def test_delete_size_1_becomes_empty() -> None:
    ll = CircularDoublyLinkedList.from_items([99])
    assert ll.head is not None

    ll.delete(ll.head)

    assert ll.size == 0
    assert ll.head is None
    assert list(ll) == []


def test_delete_node_not_in_list_raises() -> None:
    ll = CircularDoublyLinkedList.from_items([1, 2, 3])
    rogue = Node(999)

    with pytest.raises(ValueError):
        ll.delete(rogue)
