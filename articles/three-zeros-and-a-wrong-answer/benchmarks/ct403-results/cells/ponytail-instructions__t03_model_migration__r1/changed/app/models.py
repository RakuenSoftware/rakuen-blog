"""Models."""
class User:
    def __init__(self, uid, first_name=None, last_name=None, email=None, *, name=None):
        if name is not None:
            if first_name is not None or last_name is not None:
                raise TypeError("use name or first_name/last_name, not both")
            first_name = name
        elif email is None:  # Legacy User(uid, name, email) call.
            email, last_name = last_name, None

        self.uid, self.email = uid, email
        if last_name is None:
            self.name = first_name or ""
        else:
            self.first_name, self.last_name = first_name or "", last_name

    @property
    def name(self):
        return " ".join(part for part in (self.first_name, self.last_name) if part)

    @name.setter
    def name(self, value):
        parts = value.split(maxsplit=1)
        self.first_name = parts[0] if parts else ""
        self.last_name = parts[1] if len(parts) == 2 else ""

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
        if row.get("first_name") is not None or row.get("last_name") is not None:
            return cls(
                row["id"],
                row.get("first_name") or "",
                row.get("last_name") or "",
                row["email"],
            )
        return cls(row["id"], name=row["name"], email=row["email"])

class Item:
    def __init__(self, iid, owner, title):
        self.iid, self.owner, self.title = iid, owner, title
    def to_dict(self):
        return {"id": self.iid, "owner": self.owner, "title": self.title}
