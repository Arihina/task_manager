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

        try:
            with open(FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump(tasks, file, ensure_ascii=False)
        except IOError:
            raise IOError('Ошибка при записи в файл tasks.json')

    @staticmethod
    def update_task(id: int, title: str | None, description: str | None, category: str | None,
                    priority: Priority | None, due_date: str | None) -> None:
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        f = False
        for task in tasks:
            if task['id'] == id:
                if title is not None:
                    task['title'] = title
                if description is not None:
                    task['description'] = description
                if category is not None:
                    task['category'] = category
                if priority is not None:
                    task['priority'] = priority.value
                if due_date is not None:
                    task['due_date'] = due_date

                f = True
                break

        if not f:
            raise TaskNotFoundError(f'Задача с id {id} не найдена')

        try:
            with open(FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump(tasks, file, ensure_ascii=False)
        except IOError as ex:
            raise IOError('Ошибка при записи в файл tasks.json')

    @staticmethod
    def update_status(id: int) -> None:
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        f = False
        for task in tasks:
            if task['id'] == id:
                task['status'] = Status.COMPLETED.value if task.get(
                    'status') != Status.COMPLETED.value else Status.NOT_COMPLETED.value
                f = True
                break

        if not f:
            raise TaskNotFoundError(f'Задача с id {id} не найдена')

        try:
            with open(FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump(tasks, file, ensure_ascii=False, indent=4)
        except IOError as ex:
            raise IOError('Ошибка при записи в файл tasks.json')
