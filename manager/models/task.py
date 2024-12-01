from dataclasses import dataclass, field

from manager.models.priority import Priority
from manager.models.status import Status


@dataclass
class Task:
    title: str
    description: str
    category: str
    priority: Priority
    due_date: str
    status: Status = Status.NOT_COMPLETED.value
    id: int = field(init=False)

    def __post_init__(self):
        self.id = id(self)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'priority': self.priority.value,
            'due_date': self.due_date,
            'status': self.status.value
        }
