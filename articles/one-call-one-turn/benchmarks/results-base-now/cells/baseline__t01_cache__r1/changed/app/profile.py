"""Profile service with a small in-process read cache."""
from app.cache import cached_profile, invalidate_profile
from app.db import get_db


def _load_profile(uid):
    db = get_db()
    db.q(f"SELECT * FROM users WHERE id={uid}")
    return db.users.get(uid)


def get_profile(uid):
    return cached_profile(uid, _load_profile)


def update_profile(uid, data):
    db = get_db()
    db.q(f"UPDATE users SET ... WHERE id={uid}")
    db.users[uid] = {**db.users.get(uid, {}), **data}
    invalidate_profile(uid)
    return db.users[uid]
