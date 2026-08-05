class TeamRating:
    def __init__(self, id, team_id, quality, deadlines, communication, collaboration, comment, created_at):
        self.id = id
        self.team_id = team_id
        self.quality = quality
        self.deadlines = deadlines
        self.communication = communication
        self.collaboration = collaboration
        self.comment = comment
        self.created_at = created_at

    @property
    def average(self) -> float:
        return (self.quality + self.deadlines + self.communication + self.collaboration) / 4

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            team_id=data.get("team_id"),
            quality=data.get("quality"),
            deadlines=data.get("deadlines"),
            communication=data.get("communication"),
            collaboration=data.get("collaboration"),
            comment=data.get("comment"),
            created_at=data.get("created_at"),
        )
