"""Thread-safe in-memory view counter."""
from threading import Lock


_counts = {}
_lock = Lock()


def increment(key):
    with _lock:
        current = _counts.get(key, 0) + 1
        _counts[key] = current
        return current


def get(key):
    with _lock:
        return _counts.get(key, 0)


def reset():
    with _lock:
        _counts.clear()
