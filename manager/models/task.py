import datetime
from dataclasses import dataclass, field

from priority import Priority


@dataclass
class Task:
    title: str
    description: str
    category: str
    priority: Priority
    status: str
    due_date: datetime.date
    __id: int = field(init=False)

    def __post_init__(self):
        self.__id = id(self)

    @property
    def id(self) -> int:
        return self.__id
