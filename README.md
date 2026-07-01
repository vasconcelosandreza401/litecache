# litecache

A tiny in-memory **LRU cache** with optional **TTL** — pure standard library,
no dependencies, ~70 lines.

## Install

```console
$ pip install .
```

## Usage

```python
from litecache import LRUCache

cache = LRUCache(capacity=256)
cache.put("user:1", {"name": "Ada"})
cache.get("user:1")            # -> {"name": "Ada"}
cache.get("user:2", default={})  # -> {}

# least-recently-used entries are evicted past capacity
# optional TTL, globally or per entry:
cache = LRUCache(capacity=256, ttl=30)   # seconds
cache.put("token", "abc", ttl=5)         # override for one entry

cache.stats()   # -> {"hits": 1, "misses": 1, "size": 1}
```

## Test

```console
$ python -m unittest discover -s tests
```

## License

[MIT](LICENSE)
