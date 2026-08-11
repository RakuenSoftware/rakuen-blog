"""Application models."""


class User:
    def __init__(self, uid, first_name=None, last_name=None, email=None, *, name=None):
        # Keep the old User(uid, name, email) call shape working while callers
        # migrate to User(uid, first_name, last_name, email).
        if name is not None:
            if first_name is not None:
                raise TypeError("provide either first_name or name, not both")
            first_name, last_name = self._split_name(name)
        elif email is None:
            email = last_name
            first_name, last_name = self._split_name(first_name)

        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    @staticmethod
    def _split_name(name):
        parts = name.split(None, 1)
        if not parts:
            return "", ""
        if len(parts) == 1:
            return parts[0], ""
        return parts[0], parts[1]

    @property
    def name(self):
        """The legacy display-name field retained for API compatibility."""
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
        if "name" in row:
            legacy_first, legacy_last = cls._split_name(row["name"])
        else:
            legacy_first, legacy_last = "", ""

        return cls(
            row["id"],
            row.get("first_name", legacy_first),
            row.get("last_name", legacy_last),
            row["email"],
        )


class Item:
    def __init__(self, iid, owner, title):
        self.iid, self.owner, self.title = iid, owner, title
    def to_dict(self):
        return {"id": self.iid, "owner": self.owner, "title": self.title}
