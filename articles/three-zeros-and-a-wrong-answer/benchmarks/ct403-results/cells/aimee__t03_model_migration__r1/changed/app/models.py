"""Service models."""


class User:
    def __init__(
        self, uid, first_name=None, last_name=None, email=None, *, name=None
    ):
        """Create a user, accepting both split and legacy name arguments.

        The three-positional-argument form is kept for callers using the old
        ``User(uid, name, email)`` interface. New callers should pass four
        arguments or use the split-name keywords.
        """
        if name is not None:
            if first_name is not None or last_name is not None:
                raise TypeError("name cannot be combined with split name fields")
            first_name, last_name = self._split_name(name)
        elif email is None and last_name is not None:
            # In the old signature the third positional argument was email.
            email = last_name
            first_name, last_name = self._split_name(first_name)

        self.uid = uid
        self.first_name = first_name or ""
        self.last_name = last_name or ""
        self.email = email

    @staticmethod
    def _split_name(name):
        parts = (name or "").strip().split(maxsplit=1)
        if not parts:
            return "", ""
        return parts[0], parts[1] if len(parts) == 2 else ""

    @property
    def name(self):
        """The legacy full-name view retained for existing API consumers."""
        return " ".join(part for part in (self.first_name, self.last_name) if part)

    @name.setter
    def name(self, value):
        self.first_name, self.last_name = self._split_name(value)

    def to_dict(self):
        # Dual-write during the migration: new code gets structured names and
        # existing consumers can continue reading the full ``name`` field.
        return {
            "id": self.uid,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "name": self.name,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, row):
        if "first_name" not in row and "last_name" not in row:
            first_name, last_name = cls._split_name(row["name"])
        else:
            first_name = row.get("first_name")
            last_name = row.get("last_name")

            # Tolerate partially migrated rows by filling a missing component
            # from the legacy value when it is still available.
            if (first_name is None or last_name is None) and "name" in row:
                legacy_first, legacy_last = cls._split_name(row["name"])
                if first_name is None:
                    first_name = legacy_first
                if last_name is None:
                    last_name = legacy_last

        return cls(
            uid=row["id"],
            first_name=first_name or "",
            last_name=last_name or "",
            email=row["email"],
        )


class Item:
    def __init__(self, iid, owner, title):
        self.iid, self.owner, self.title = iid, owner, title
    def to_dict(self):
        return {"id": self.iid, "owner": self.owner, "title": self.title}
