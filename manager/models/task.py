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
