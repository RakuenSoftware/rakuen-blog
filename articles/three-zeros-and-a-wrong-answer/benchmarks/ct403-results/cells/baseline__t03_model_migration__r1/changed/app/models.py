"""Models used by the service."""


class User:
    def __init__(
        self, uid, first_name=None, last_name=None, email=None, *, name=None
    ):
        """Create a user while accepting both old and new calling conventions.

        The old constructor was ``User(uid, name, email)``.  Keeping that form
        valid lets callers migrate independently from stored rows and API
        responses.
        """
        if name is not None:
            if first_name is not None or last_name is not None:
                raise TypeError("provide name or first_name/last_name, not both")
            first_name, last_name = self._split_name(name)
        elif email is None and last_name is not None:
            # Backwards compatibility for User(uid, name, email).
            email = last_name
            first_name, last_name = self._split_name(first_name)

        self.uid = uid
        self.first_name = first_name or ""
        self.last_name = last_name or ""
        self.email = email

    @staticmethod
    def _split_name(name):
        first_name, separator, last_name = (name or "").partition(" ")
        return first_name, last_name if separator else ""

    @property
    def name(self):
        """Legacy combined name retained for callers during the migration."""
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
            legacy_first_name, legacy_last_name = cls._split_name(row.get("name"))
            return cls(
                uid=row["id"],
                first_name=(
                    legacy_first_name
                    if row.get("first_name") is None
                    else row["first_name"]
                ),
                last_name=(
                    legacy_last_name
                    if row.get("last_name") is None
                    else row["last_name"]
                ),
                email=row["email"],
            )
        return cls(uid=row["id"], name=row["name"], email=row["email"])


class Item:
    def __init__(self, iid, owner, title):
        self.iid, self.owner, self.title = iid, owner, title
    def to_dict(self):
        return {"id": self.iid, "owner": self.owner, "title": self.title}
