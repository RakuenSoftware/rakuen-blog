"""Models."""
class User:
    def __init__(self, uid, first_name, last_name, email):
        self.uid, self.first_name, self.last_name, self.email = uid, first_name, last_name, email

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
        if "first_name" in row:
            return cls(row["id"], row["first_name"], row["last_name"], row["email"])
        first_name, _, last_name = row["name"].partition(" ")
        return cls(row["id"], first_name, last_name, row["email"])

class Item:
    def __init__(self, iid, owner, title):
        self.iid, self.owner, self.title = iid, owner, title
    def to_dict(self):
        return {"id": self.iid, "owner": self.owner, "title": self.title}
