"""Service models."""


class User:
    def __init__(self, uid, first_name, last_name, email):
        self.uid = uid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    @property
    def name(self):
        """The legacy full-name representation kept for existing callers."""
        return " ".join(part for part in (self.first_name, self.last_name) if part)

    @name.setter
    def name(self, value):
        """Keep assignments by older callers in sync with the split fields."""
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
        if "first_name" in row and "last_name" in row:
            first_name = row["first_name"]
            last_name = row["last_name"]
        else:
            first_name, last_name = cls._split_name(row["name"])
        return cls(row["id"], first_name, last_name, row["email"])

    @staticmethod
    def _split_name(name):
        first_name, separator, last_name = name.strip().partition(" ")
        return first_name, last_name.lstrip() if separator else ""


class Item:
    def __init__(self, iid, owner, title):
        self.iid, self.owner, self.title = iid, owner, title
    def to_dict(self):
        return {"id": self.iid, "owner": self.owner, "title": self.title}
