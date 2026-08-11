"""Models."""
class User:
    def __init__(self, uid, first_name, last_name=None, email=None):
        if email is None:  # Legacy User(uid, name, email) callers.
            first_name, _, inferred_last_name = first_name.partition(" ")
            email, last_name = last_name, inferred_last_name
        self.uid, self.first_name, self.last_name, self.email = uid, first_name, last_name, email

    @property
    def name(self):
        return " ".join(filter(None, (self.first_name, self.last_name)))

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
        first_name, _, last_name = row["name"].partition(" ")
        return cls(row["id"], first_name, last_name, row["email"])

class Item:
    def __init__(self, iid, owner, title):
        self.iid, self.owner, self.title = iid, owner, title
    def to_dict(self):
        return {"id": self.iid, "owner": self.owner, "title": self.title}
