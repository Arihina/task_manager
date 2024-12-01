import json
import os

from manager.exceptions.tasks_exceptions import TaskNotFoundError
from manager.models.priority import Priority
from manager.models.status import Status
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

    @staticmethod
    def get_current_tasks():
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        return [task for task in tasks if task['status'] == Status.NOT_COMPLETED.value]


class Writer:

    @staticmethod
    def add_task(task: Task) -> None:
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        tasks.append(task.to_dict())

        with open(FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(tasks, file, ensure_ascii=False)

    @staticmethod
    def remove_task_by_id(id: int) -> None:
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        f = False
        for task in tasks:
            if task['id'] == id:
                tasks.remove(task)
                f = True
                break

        if f is False:
            raise TaskNotFoundError(f'Не найдена задача с id {id}')

        try:
            with open(FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump(tasks, file, ensure_ascii=False)
        except IOError as ex:
            raise IOError('Ошибка при записи в файл tasks.json')

    @staticmethod
    def remove_tasks_by_category(category: str) -> None:
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        f = False
        for task in tasks:
            if task['category'] == category:
                tasks.remove(task)
                f = True

        if f is False:
            raise TaskNotFoundError(f'Не найдены задача с категорией {category}')

        with open(FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(tasks, file, ensure_ascii=False)
