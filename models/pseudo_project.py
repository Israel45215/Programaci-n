class PseudoProject:
    def __init__(self, id, project_id, team_id, name, description, status):
        self.id = id
        self.project_id = project_id
        self.team_id = team_id
        self.name = name
        self.description = description
        self.status = status

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            project_id=data.get("project_id"),
            team_id=data.get("team_id"),
            name=data.get("name"),
            description=data.get("description"),
            status=data.get("status"),
        )