"""litecache — a tiny in-memory LRU cache with optional TTL.

Standard library only.
"""
import time
from collections import OrderedDict

__all__ = ["LRUCache"]
__version__ = "0.1.0"

_MISSING = object()


class LRUCache:
    """A fixed-capacity LRU cache with optional per-entry TTL and stats."""

    def __init__(self, capacity=128, ttl=None):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if ttl is not None and ttl <= 0:
            raise ValueError("ttl must be positive or None")
        self.capacity = capacity
        self.ttl = ttl
        self._data = OrderedDict()
        self.hits = 0
        self.misses = 0

    def __len__(self):
        return len(self._data)

    @staticmethod
    def _expired(expires_at):
        return expires_at is not None and time.monotonic() >= expires_at

    def __contains__(self, key):
        entry = self._data.get(key)
        if entry is None:
            return False
        if self._expired(entry[1]):
            del self._data[key]
            return False
        return True

    def get(self, key, default=None):
        entry = self._data.get(key)
        if entry is None or self._expired(entry[1]):
            if entry is not None:
                del self._data[key]
            self.misses += 1
            return default
        self._data.move_to_end(key)
        self.hits += 1
        return entry[0]

    def peek(self, key, default=None):
        """Return a value without updating LRU order or hit/miss stats."""
        entry = self._data.get(key)
        if entry is None or self._expired(entry[1]):
            return default
        return entry[0]

    def put(self, key, value, ttl=_MISSING):
        effective = self.ttl if ttl is _MISSING else ttl
        expires_at = time.monotonic() + effective if effective is not None else None
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = (value, expires_at)
        while len(self._data) > self.capacity:
            self._data.popitem(last=False)

    def pop(self, key, default=None):
        """Remove `key` and return its value, or `default` if absent/expired."""
        entry = self._data.pop(key, None)
        if entry is None or self._expired(entry[1]):
            return default
        return entry[0]

    def clear(self):
        self._data.clear()
        self.hits = 0
        self.misses = 0

    def stats(self):
        return {"hits": self.hits, "misses": self.misses, "size": len(self._data)}
