"""Doubly-linked circular list for the pruning step (SPEC 5.8).

The pruning step needs to delete the "middle" of a 3-node window and then
rewind one node. A circular, doubly-linked list makes this operation direct
and keeps the implementation close to the paper.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class Node(Generic[T]):
    item: T
    next: Node[T] = field(init=False, repr=False)
    prev: Node[T] = field(init=False, repr=False)
    _owner: CircularDoublyLinkedList[T] | None = field(
        default=None, init=False, repr=False, compare=False
    )

    def __post_init__(self) -> None:
        self.next = self
        self.prev = self

    def iter_cycle(self) -> Iterator[Node[T]]:
        """Yield nodes exactly once around the cycle, starting from this node."""

        yield self
        node = self.next
        while node is not self:
            yield node
            node = node.next


@dataclass(slots=True)
class CircularDoublyLinkedList(Generic[T]):
    head: Node[T] | None = None
    size: int = 0

    @classmethod
    def from_items(cls, items: Iterable[T]) -> CircularDoublyLinkedList[T]:
        ll: CircularDoublyLinkedList[T] = cls()

        iterator = iter(items)
        try:
            first_item = next(iterator)
        except StopIteration:
            return ll

        head = Node(first_item)
        ll.head = head
        ll.size = 1
        head._owner = ll

        tail = head
        for item in iterator:
            node = Node(item)
            node._owner = ll

            node.prev = tail
            node.next = head
            tail.next = node
            head.prev = node

            tail = node
            ll.size += 1

        return ll

    def __iter__(self) -> Iterator[T]:
        if self.head is None:
            return
        for node in self.head.iter_cycle():
            yield node.item

    def delete(self, node: Node[T]) -> None:
        """Remove `node` from the list.

        Raises:
            ValueError: if the node is not owned by this list.
        """

        if node._owner is not self:
            raise ValueError("node is not part of this list")

        if self.size <= 0 or self.head is None:
            raise RuntimeError("internal error: list is empty but has owned nodes")

        if self.size == 1:
            self.head = None
            self.size = 0
            node._owner = None
            node.next = node
            node.prev = node
            return

        next_node = node.next
        prev_node = node.prev

        prev_node.next = next_node
        next_node.prev = prev_node

        if self.head is node:
            self.head = next_node

        self.size -= 1

        node._owner = None
        node.next = node
        node.prev = node
