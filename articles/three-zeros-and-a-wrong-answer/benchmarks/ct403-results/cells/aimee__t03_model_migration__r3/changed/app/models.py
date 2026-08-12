"""Models."""
class User:
    def __init__(self, uid, first_name=None, last_name=None, email=None, *, name=None):
        # Accept the old User(uid, name, email) and User(..., name=...) forms
        # while callers move to the split fields.
        if name is not None:
            if first_name is not None or last_name is not None:
                raise TypeError("use either name or first_name/last_name")
            first_name, last_name = self._split_name(name)
        elif email is None:
            email = last_name
            first_name, last_name = self._split_name(first_name)

        self.uid = uid
        self.first_name = first_name or ""
        self.last_name = last_name or ""
        self.email = email

    @staticmethod
    def _split_name(name):
        parts = (name or "").strip().split(maxsplit=1)
        return (parts[0], parts[1] if len(parts) == 2 else "") if parts else ("", "")

    @property
    def name(self):
        """Legacy full-name view retained for callers during the migration."""
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
        if "first_name" not in row and "last_name" not in row:
            first_name, last_name = cls._split_name(row["name"])
        else:
            legacy_first, legacy_last = cls._split_name(row.get("name"))
            first_name = row.get("first_name", legacy_first)
            last_name = row.get("last_name", legacy_last)
        return cls(row["id"], first_name, last_name, row["email"])

class Item:
    def __init__(self, iid, owner, title):
        self.iid, self.owner, self.title = iid, owner, title
    def to_dict(self):
        return {"id": self.iid, "owner": self.owner, "title": self.title}
