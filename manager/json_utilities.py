import json
import os

from manager.models.task import Task

FILE_PATH = os.path.join(os.path.dirname(__file__), '../resources/tasks.json')


class Reader:
    @staticmethod
    def get_task_by_id(id: int) -> Task | None:
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        for task in tasks:
            if task['id'] == id:
                return task

    @staticmethod
    def get_tasks_by_category(category: str) -> list[Task]:
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        return [task for task in tasks if task['category'] == category]


class Writer:

    @staticmethod
    def add_task(task: Task) -> None:
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        tasks.append(task.__dict__)

        with open(FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(tasks, file, ensure_ascii=False, indent=4)

    @staticmethod
    def remove_task(id: int | None, category: str | None) -> None:
        pass