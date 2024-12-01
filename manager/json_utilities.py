import json
import os

from manager.models.task import Task

FILE_PATH = os.path.join(os.path.dirname(__file__), '../resources/tasks.json')


class Reader:
    pass


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
