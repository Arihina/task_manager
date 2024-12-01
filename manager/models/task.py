import datetime
from dataclasses import dataclass, field

from priority import Priority
from status import Status


@dataclass
class Task:
    title: str
    description: str
    category: str
    priority: Priority
    due_date: datetime.date
    status: Status = Status.NOT_COMPLETED
    id: int = field(init=False)

    def __post_init__(self):
        self.id = id(self)
