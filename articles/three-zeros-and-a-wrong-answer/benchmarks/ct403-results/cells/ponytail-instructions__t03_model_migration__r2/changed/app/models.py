"""Models."""
_MISSING = object()


class User:
    def __init__(self, uid, first_name, last_name, email=_MISSING):
        # Keep the old User(uid, name, email) call shape during migration.
        if email is _MISSING:
            name, email = first_name, last_name
            first_name, last_name = self._split_name(name)
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    @staticmethod
    def _split_name(name):
        parts = name.split(None, 1)
        return (parts[0], parts[1] if len(parts) == 2 else "") if parts else ("", "")

    @property
    def name(self):
        return " ".join(part for part in (self.first_name, self.last_name) if part)

    def to_dict(self):
        return {
            "id": self.uid,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "name": self.name,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, row):
        if "first_name" in row or "last_name" in row:
            return cls(row["id"], row.get("first_name", ""), row.get("last_name", ""), row["email"])
        first_name, last_name = cls._split_name(row["name"])
        return cls(row["id"], first_name, last_name, row["email"])


class Item:
    def __init__(self, iid, owner, title):
        self.iid, self.owner, self.title = iid, owner, title
    def to_dict(self):
        return {"id": self.iid, "owner": self.owner, "title": self.title}
