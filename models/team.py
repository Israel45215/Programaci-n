class Team:
    def __init__(self, id, name, description, members):
        self.id = id
        self.name = name
        self.description = description
        self.members = members

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            members=data.get("members"),
        )