"""Small caches used by profile and catalog code.

The implementations are deliberately incomplete; tickets exercise invalidation,
expiry, stampede prevention, and lock granularity independently.
"""
import threading
import time

_profile_cache = {}
_catalog_cache = {}
_profile_lock = threading.Lock()
_catalog_lock = threading.Lock()


def cached_profile(uid, loader):
    with _profile_lock:
        if uid not in _profile_cache:
            _profile_cache[uid] = loader(uid)
        return _profile_cache[uid]


def invalidate_profile(uid):
    with _profile_lock:
        _profile_cache.pop(uid, None)


def ttl_get(key, loader, ttl=60, now=time.monotonic):
    entry = _catalog_cache.get(key)
    if entry:
        return entry[1]
    value = loader(key)
    _catalog_cache[key] = (now(), value)
    return value


def stampede_get(key, loader, ttl=60, now=time.monotonic):
    entry = _catalog_cache.get(key)
    if entry and now() - entry[0] < ttl:
        return entry[1]
    value = loader(key)
    _catalog_cache[key] = (now(), value)
    return value


def per_key_get(key, loader):
    with _catalog_lock:
        return loader(key)


def reset():
    with _profile_lock:
        _profile_cache.clear()
    _catalog_cache.clear()
