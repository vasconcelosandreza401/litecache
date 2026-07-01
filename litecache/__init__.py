"""litecache — a tiny in-memory LRU cache.

Standard library only.
"""
from collections import OrderedDict

__all__ = ["LRUCache"]
__version__ = "0.1.0"


class LRUCache:
    """A fixed-capacity least-recently-used cache."""

    def __init__(self, capacity=128):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._data = OrderedDict()

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data

    def get(self, key, default=None):
        if key not in self._data:
            return default
        self._data.move_to_end(key)
        return self._data[key]

    def put(self, key, value):
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value
        while len(self._data) > self.capacity:
            self._data.popitem(last=False)

    def clear(self):
        self._data.clear()
