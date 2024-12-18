import json
import os

from manager.exceptions.tasks_exceptions import TaskNotFoundError
from manager.models.priority import Priority
from manager.models.status import Status
from manager.models.task import Task, OutputTask


class Loader:
    @staticmethod
    def load_task(task_data: dict) -> OutputTask:
        if task_data['priority'] == 'низкий':
            priority = Priority.LOW
        elif task_data['priority'] == 'средний':
            priority = Priority.MEDIUM
        else:
            priority = Priority.HIGH

        if task_data['status'] == 'Выполнена':
            status = Status.COMPLETED
        else:
            status = Status.NOT_COMPLETED

        return OutputTask(
            title=task_data['title'],
            description=task_data['description'],
            category=task_data['category'],
            priority=priority,
            due_date=task_data['due_date'],
            status=status,
            id=task_data['id']
        )


class Reader:
    FILE_PATH = os.path.join(os.path.dirname(__file__), '../resources/tasks.json')

    @staticmethod
    def set_file_path(path: str) -> None:
        Reader.FILE_PATH = path

    @staticmethod
    def get_task_by_id(id: int) -> Task | None:
        try:
            with open(Reader.FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        for task in tasks:
            if task['id'] == id:
                return task

    @staticmethod
    def get_tasks_by_category(category: str) -> list[OutputTask]:
        try:
            with open(Reader.FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        return [Loader.load_task(task) for task in tasks if task['category'] == category]

    @staticmethod
    def get_current_tasks() -> list[OutputTask]:
        try:
            with open(Reader.FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        return [Loader.load_task(task) for task in tasks if task['status'] == Status.NOT_COMPLETED.value]

    @staticmethod
    def search_by_title(title: str) -> list[OutputTask]:
        try:
            with open(Reader.FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        return [Loader.load_task(task) for task in tasks if title.lower() in task['title'].lower()]

    @staticmethod
    def search_by_description(description: str) -> list[OutputTask]:
        try:
            with open(Reader.FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        return [Loader.load_task(task) for task in tasks if description.lower() in task['description'].lower()]

    @staticmethod
    def search_by_category(category: str) -> list[OutputTask]:
        try:
            with open(Reader.FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        return [Loader.load_task(task) for task in tasks if category.lower() in task['category'].lower()]

    @staticmethod
    def search_key_word(word: str) -> list[OutputTask]:
        try:
            with open(Reader.FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        filter_tasks = []

        for task in tasks:
            if word.lower() in task['title'].lower() or word.lower() in task['description'].lower() or word.lower() in \
                    task['category'].lower():
                filter_tasks.append(Loader.load_task(task))

        return filter_tasks

    @staticmethod
    def filter_by_category() -> dict[str, list[OutputTask]]:
        try:
            with open(Reader.FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        filter_tasks = {}

        for task in tasks:
            category = task.get('category')
            if category:
                if category not in filter_tasks:
                    filter_tasks[category] = []
                filter_tasks[category].append(Loader.load_task(task))

        return filter_tasks

    @staticmethod
    def search_by_status(status: int) -> list[OutputTask]:
        if status == 1:
            status = Status.COMPLETED.value
        else:
            status = Status.NOT_COMPLETED.value

        try:
            with open(Reader.FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        return [Loader.load_task(task) for task in tasks if status == task['status']]


class Writer:
    FILE_PATH = os.path.join(os.path.dirname(__file__), '../resources/tasks.json')

    @staticmethod
    def set_file_path(path: str):
        Reader.FILE_PATH = path

    @staticmethod
    def add_task(task: Task) -> None:
        try:
            with open(Writer.FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        tasks.append(task.to_dict())

        with open(Writer.FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(tasks, file, ensure_ascii=False)

    @staticmethod
    def remove_task_by_id(id: int) -> None:
        try:
            with open(Writer.FILE_PATH, 'r', encoding='utf-8') as file:
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
            with open(Writer.FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump(tasks, file, ensure_ascii=False)
        except IOError as ex:
            raise IOError('Ошибка при записи в файл tasks.json')

    @staticmethod
    def remove_tasks_by_category(category: str) -> None:
        try:
            with open(Writer.FILE_PATH, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')

        filter_tasks = [task for task in tasks if task['category'] != category]

        if len(filter_tasks) == len(tasks):
            raise TaskNotFoundError(f'Не найдены задачи с категорией {category}')

        try:
            with open(Writer.FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump(filter_tasks, file, ensure_ascii=False)
        except (FileNotFoundError, json.JSONDecodeError):
            raise FileNotFoundError('Не найден файл tasks.json в папке resources')
        except IOError:
            raise IOError('Ошибка при записи в файл tasks.json')

    @staticmethod
    def update_task(id: int, title: str | None, description: str | None, category: str | None,
                    priority: Priority | None, due_date: str | None) -> None:
        try:
            with open(Writer.FILE_PATH, 'r', encoding='utf-8') as file:
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
            with open(Writer.FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump(tasks, file, ensure_ascii=False)
        except IOError as ex:
            raise IOError('Ошибка при записи в файл tasks.json')

    @staticmethod
    def update_status(id: int) -> None:
        try:
            with open(Writer.FILE_PATH, 'r', encoding='utf-8') as file:
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
            with open(Writer.FILE_PATH, 'w', encoding='utf-8') as file:
                json.dump(tasks, file, ensure_ascii=False, indent=4)
        except IOError as ex:
            raise IOError('Ошибка при записи в файл tasks.json')
