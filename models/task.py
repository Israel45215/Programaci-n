class Task:
    def __init__(self, id, title, pseudo_project_id, assigned, status, priority, progress, start_date, date):
        self.id = id
        self.title = title
        self.pseudo_project_id = pseudo_project_id
        self.assigned = assigned
        self.status = status
        self.priority = priority
        self.progress = progress
        self.start_date = start_date
        self.date = date

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            pseudo_project_id=data.get("pseudo_project_id"),
            assigned=data.get("assigned"),
            status=data.get("status"),
            priority=data.get("priority"),
            progress=data.get("progress"),
            start_date=data.get("start_date"),
            date=data.get("date"),
        )