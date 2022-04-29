"""A leftist heap."""

from __future__ import annotations
from dataclasses import (
    dataclass, field
)
from typing import (
    Protocol, TypeVar, Generic, Union,
    Optional,
    Any
)


# Some type stuff
class Ordered(Protocol):
    """Types that support < comparison."""

    def __lt__(self, other: Any) -> bool:
        """Determine if self is < other."""
        ...


Ord = TypeVar('Ord', bound=Ordered)

# Heap structure


class EmptyClass(Generic[Ord]):
    """Empty heap."""

    # This is some magick to ensure we never have more
    # than one empty heap.
    _instance: Optional[EmptyClass[Any]] = None

    def __new__(cls) -> EmptyClass[Any]:
        """Create a new empty heap."""
        if cls._instance is None:
            cls._instance = super(EmptyClass, cls).__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        """Return 'Empty'."""
        return "Empty"

    @property
    def rank(self) -> int:
        """Return 0.

        The rank of an empty heap is always zero, and
        implemented this way it always will be. You can
        access it with tree.rank but you cannot change it.
        """
        return 0

    @property
    def value(self) -> Ord:
        """Raise exception."""
        raise AttributeError("No value on an empty heap")

    @property
    def left(self) -> HeapNode[Ord]:
        """Raise exception."""
        raise AttributeError("No left on an empty heap")

    @property
    def right(self) -> HeapNode[Ord]:
        """Raise exception."""
        raise AttributeError("No right on an empty heap")


# This is the one and only empty heap
Empty = EmptyClass()


@dataclass
class InnerNode(Generic[Ord]):
    """Inner node in the heap."""

    value: Ord
    left: HeapNode[Ord] = Empty
    right: HeapNode[Ord] = Empty
    rank: int = field(init=False)  # Don't set in init, fix in post_init.

    def __post_init__(self) -> None:
        """Fix consistency after creation."""
        self.rank = 1 + self.right.rank


# A HeapNode is either an inner node or an empty heap
HeapNode = Union[InnerNode[Ord], EmptyClass]


# The actual functionality
def merge(left: HeapNode[Ord], right: HeapNode[Ord]) -> HeapNode[Ord]:
    """Merge two heaps into one."""
    # FIXME: The merge doesn't restore the leftst property if it is
    # violated. You need to fix that.
    return right \
        if left is Empty \
        else left \
        if right is Empty \
        else InnerNode(left.value, left.left, merge(left.right, right)) \
        if left.value < right.value \
        else InnerNode(right.value, right.left, merge(left, right.right))


def restore(n: HeapNode[Ord]) -> HeapNode[Ord]:
    """
    Restore the leftist property for n.

    This means ensuring that the n.left.rank > n.right.rank
    when n is an inner node (n is not Empty).
    """
    # FIXME: you need to implement this
    ...


class Heap(Generic[Ord]):
    """Wrapper class for heap functionality."""

    heap: HeapNode[Ord]

    def __init__(self) -> None:
        """Create empty heap."""
        self.heap = Empty

    def insert(self, val: Ord) -> None:
        """Add new value to the heap."""
        self.heap = merge(self.heap, InnerNode(val))

    def get_min(self) -> Ord:
        """Get the minimal value."""
        return self.heap.value

    def delete_min(self) -> Ord:
        """Get and delete the minimal value."""
        val, self.heap = \
            self.heap.value, merge(self.heap.left, self.heap.right)
        return val

    def __bool__(self) -> bool:
        """Return true when non-empty."""
        return self.heap is not Empty


def heap_sort(x: list[Ord]) -> list[Ord]:
    """Do basic heap sort."""
    heap = Heap[Ord]()
    for a in x:
        heap.insert(a)

    res = []
    while heap:
        res.append(heap.delete_min())
    return res
