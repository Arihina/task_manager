import json

import pytest

from manager.exceptions.tasks_exceptions import TaskNotFoundError
from manager.json_utilities import Writer
from manager.models.priority import Priority
from manager.models.status import Status
from manager.models.task import Task

test_tasks = [
    {"title": "Тестовая задача 1", "description": "Описание задачи 1", "category": "Работа",
     "status": "Не выполнена", "priority": Priority.LOW.value},
    {"title": "Тестовая задача 2", "description": "Описание задачи 2", "category": "Личное",
     "status": "Выполнена", "priority": Priority.HIGH.value},
]


@pytest.fixture
def setup_tasks(tmp_path):
    file_path = tmp_path / "tasks.json"

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(test_tasks, file)

    Writer.set_file_path(str(file_path))

    return file_path


def test_add_task(setup_tasks):
    new_task = Task(title="Новая задача", description="Описание новой задачи", category="Работа",
                    status=Status.NOT_COMPLETED, priority=Priority.MEDIUM, due_date="2024-12-12")
    Writer.add_task(new_task)

    tasks = json.load(open(setup_tasks, 'r', encoding='utf-8'))

    assert len(tasks) == 2
    assert tasks[1]['title'] == "Тестовая задача 2"


def test_remove_task_by_id_not_found(setup_tasks):
    with pytest.raises(TaskNotFoundError):
        Writer.remove_task_by_id(999)


def test_remove_tasks_by_category(setup_tasks):
    Writer.remove_tasks_by_category("Работа")

    tasks = json.load(open(setup_tasks, 'r', encoding='utf-8'))

    assert len(tasks) == 2


def test_remove_tasks_by_category_not_found(setup_tasks):
    with pytest.raises(TaskNotFoundError):
        Writer.remove_tasks_by_category("Не существующая категория")


def test_update_task_not_found(setup_tasks):
    with pytest.raises(TaskNotFoundError):
        Writer.update_task(999, title="Обновленная задача", description=None, category=None, priority=None,
                           due_date=None)


def test_update_status_not_found(setup_tasks):
    with pytest.raises(TaskNotFoundError):
        Writer.update_status(999)


if __name__ == '__main__':
    pytest.main()
