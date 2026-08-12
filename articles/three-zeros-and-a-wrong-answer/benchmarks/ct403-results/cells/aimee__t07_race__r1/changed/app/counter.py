"""Thread-safe in-memory view counter."""

from threading import Lock


_counts = {}
_lock = Lock()


def increment(key):
    with _lock:
        current = _counts.get(key, 0)
        _counts[key] = current + 1
        return _counts[key]


def get(key):
    with _lock:
        return _counts.get(key, 0)


def reset():
    with _lock:
        _counts.clear()
