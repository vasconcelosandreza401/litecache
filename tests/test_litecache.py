import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from litecache import LRUCache, memoize  # noqa: E402


class TestLRUCache(unittest.TestCase):
    def test_get_put(self):
        c = LRUCache(2)
        c.put("a", 1)
        self.assertEqual(c.get("a"), 1)
        self.assertEqual(c.get("missing", "d"), "d")

    def test_capacity_eviction(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("b", 2)
        c.put("c", 3)
        self.assertNotIn("a", c)
        self.assertIn("b", c)
        self.assertIn("c", c)

    def test_lru_order(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("b", 2)
        c.get("a")
        c.put("c", 3)
        self.assertIn("a", c)
        self.assertNotIn("b", c)

    def test_ttl_expiry(self):
        c = LRUCache(10, ttl=0.02)
        c.put("x", 1)
        self.assertEqual(c.get("x"), 1)
        time.sleep(0.03)
        self.assertIsNone(c.get("x"))
        self.assertNotIn("x", c)

    def test_stats(self):
        c = LRUCache(10)
        c.put("a", 1)
        c.get("a")
        c.get("nope")
        s = c.stats()
        self.assertEqual(s["hits"], 1)
        self.assertEqual(s["misses"], 1)

    def test_capacity_validation(self):
        with self.assertRaises(ValueError):
            LRUCache(0)

    def test_peek_has_no_side_effects(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("b", 2)
        self.assertEqual(c.peek("a"), 1)   # does not reorder a
        c.put("c", 3)                      # a is still LRU -> evicted
        self.assertNotIn("a", c)
        self.assertEqual(c.stats()["hits"], 0)

    def test_pop(self):
        c = LRUCache(2)
        c.put("a", 1)
        self.assertEqual(c.pop("a"), 1)
        self.assertNotIn("a", c)
        self.assertEqual(c.pop("a", "default"), "default")

    def test_memoize(self):
        calls = []

        @memoize(capacity=8)
        def square(n):
            calls.append(n)
            return n * n

        self.assertEqual(square(4), 16)
        self.assertEqual(square(4), 16)
        self.assertEqual(calls, [4])
        self.assertEqual(square.cache.stats()["hits"], 1)


if __name__ == "__main__":
    unittest.main()
