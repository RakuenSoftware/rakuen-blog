"""Application models."""

_MISSING = object()


class User:
    def __init__(
        self, uid, first_name=None, last_name=None, email=_MISSING, *, name=None
    ):
        # Keep accepting User(uid, name, email) while callers migrate to the
        # split-name constructor.
        if email is _MISSING:
            email = last_name
            first_name, last_name = self._split_name(first_name)
        elif name is not None:
            if first_name is not None:
                raise TypeError("pass either first_name or name, not both")
            first_name, last_name = self._split_name(name)

        self.uid = uid
        self.first_name = first_name or ""
        self.last_name = last_name or ""
        self.email = email

    @staticmethod
    def _split_name(name):
        parts = name.strip().split(maxsplit=1)
        if not parts:
            return "", ""
        if len(parts) == 1:
            return parts[0], ""
        return parts[0], parts[1]

    @property
    def name(self):
        """Compatibility view for code that still consumes a full name."""
        return " ".join(part for part in (self.first_name, self.last_name) if part)

    @name.setter
    def name(self, value):
        self.first_name, self.last_name = self._split_name(value)

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
            return cls(
                row["id"],
                row.get("first_name", ""),
                row.get("last_name", ""),
                row["email"],
            )
        return cls(row["id"], row["name"], row["email"])

class Item:
    def __init__(self, iid, owner, title):
        self.iid, self.owner, self.title = iid, owner, title
    def to_dict(self):
        return {"id": self.iid, "owner": self.owner, "title": self.title}
