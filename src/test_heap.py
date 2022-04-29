"""Testing the heap."""

from heap import heap_sort


def test_heap_sort() -> None:
    """Test that we can sort with the heap."""
    x = [1, 5, 2, 3, 5, 4]
    y = heap_sort(x)
    x.sort()
    assert x == y
