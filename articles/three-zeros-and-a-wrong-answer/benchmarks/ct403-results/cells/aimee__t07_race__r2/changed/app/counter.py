"""Thread-safe in-memory view counter."""
import threading


_counts = {}
_counts_lock = threading.Lock()


def increment(key):
    with _counts_lock:
        _counts[key] = _counts.get(key, 0) + 1
        return _counts[key]


def get(key):
    with _counts_lock:
        return _counts.get(key, 0)


def reset():
    with _counts_lock:
        _counts.clear()
