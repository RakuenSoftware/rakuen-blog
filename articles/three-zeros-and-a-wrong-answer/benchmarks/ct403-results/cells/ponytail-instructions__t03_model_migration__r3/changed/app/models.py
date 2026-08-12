"""Service models."""
class User:
    def __init__(self, uid, first_name=None, last_name=None, email=None, *, name=None):
        if name is not None:
            first_name, last_name = self._split_name(name)
        elif email is None:  # Legacy positional form: User(uid, name, email)
            email = last_name
            first_name, last_name = self._split_name(first_name)
        self.uid = uid
        self.first_name = first_name or ""
        self.last_name = last_name or ""
        self.email = email

    @staticmethod
    def _split_name(name):
        parts = (name or "").split(maxsplit=1)
        return (parts[0], parts[1] if len(parts) > 1 else "") if parts else ("", "")

    @property
    def name(self):
        return " ".join(filter(None, (self.first_name, self.last_name)))

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
            return cls(row["id"], row.get("first_name"), row.get("last_name"), row["email"])
        return cls(row["id"], email=row["email"], name=row["name"])

class Item:
    def __init__(self, iid, owner, title):
        self.iid, self.owner, self.title = iid, owner, title
    def to_dict(self):
        return {"id": self.iid, "owner": self.owner, "title": self.title}
