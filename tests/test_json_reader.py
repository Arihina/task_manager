import json

import pytest

from manager.json_utilities import Reader

test_tasks = [
    {"id": 1, "title": "Тестовая задача 1", "description": "Описание задачи 1", "category": "Работа",
     "status": "Не выполнена", "priority": "высокий"},
    {"id": 2, "title": "Тестовая задача 2", "description": "Описание задачи 2", "category": "Личное",
     "status": "Выполнена", "priority": "высокий"},
    {"id": 3, "title": "Тестовая задача 3", "description": "Описание задачи 3", "category": "Работа",
     "status": "Не выполнена", "priority": "высокий"},
]


@pytest.fixture
def setup_tasks(tmp_path):
    file_path = tmp_path / "tasks.json"

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(test_tasks, file)

    Reader.set_file_path(str(file_path))

    return file_path


def test_get_task_by_id(setup_tasks):
    task = Reader.get_task_by_id(1)
    assert task == test_tasks[0]

    task = Reader.get_task_by_id(999)
    assert task is None


def test_get_tasks_by_category(setup_tasks):
    tasks = Reader.get_tasks_by_category("Работа")
    assert len(tasks) == 2


def test_get_current_tasks(setup_tasks):
    tasks = Reader.get_current_tasks()
    assert len(tasks) == 2


def test_search_by_title(setup_tasks):
    tasks = Reader.search_by_title("Тест")
    assert len(tasks) == 3


def test_search_by_description(setup_tasks):
    tasks = Reader.search_by_description("задачи")
    assert len(tasks) == 3


if __name__ == '__main__':
    pytest.main()
