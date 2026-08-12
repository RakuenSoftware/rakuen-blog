"""Models."""
class User:
    def __init__(self, uid, first_name=None, last_name=None, email=None, *, name=None):
        if name is not None:
            first_name, _, last_name = name.partition(" ")
        elif email is None:  # Legacy User(uid, name, email) call.
            email = last_name
            first_name, _, last_name = first_name.partition(" ")
        self.uid, self.first_name, self.last_name, self.email = uid, first_name, last_name, email

    @property
    def name(self):
        return self.first_name + (f" {self.last_name}" if self.last_name else "")

    @name.setter
    def name(self, value):
        self.first_name, _, self.last_name = value.partition(" ")

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
        if "first_name" in row:
            return cls(row["id"], row["first_name"], row.get("last_name", ""), row["email"])
        return cls(row["id"], email=row["email"], name=row["name"])

class Item:
    def __init__(self, iid, owner, title):
        self.iid, self.owner, self.title = iid, owner, title
    def to_dict(self):
        return {"id": self.iid, "owner": self.owner, "title": self.title}
