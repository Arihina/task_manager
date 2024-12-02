import re
from datetime import datetime

from manager.exceptions.tasks_exceptions import TaskNotFoundError
from manager.json_utilities import Reader, Writer
from manager.models.priority import Priority


class ProcessingOutput:
    @staticmethod
    def is_valid_date(date_str: str) -> bool:
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(pattern, date_str):
            print("Ошибка: дата должна быть в формате 'год-месяц-день'")
            return False

        year, month, day = map(int, date_str.split('-'))

        if year <= 0 or month <= 0 or day <= 0:
            print("Ошибка: год, месяц и день должны быть целыми числами больше 0")
            return False

        if month < 1 or month > 12:
            print("Ошибка: месяц должен быть в диапазоне от 1 до 12")
            return False

        try:
            datetime(year, month, day)
        except ValueError:
            print("Ошибка: некорректная дата")
            return False

        return True

    @staticmethod
    def get_current() -> None:
        try:
            tasks = Reader.get_current_tasks()

            if len(tasks) == 0:
                print('Нет текущих задач')
            else:
                print('Текущие задачи')
                for task in tasks:
                    print(task)

        except FileNotFoundError as ex:
            print('Ошибка: не найден файл tasks.json в папке resources')

    @staticmethod
    def get_by_category() -> None:
        print('Задачи по категориям')

        try:
            tasks = Reader.filter_by_category()

            if len(tasks) == 0:
                print('Нет задач')
            else:
                for key, value in tasks.items():
                    print(f'Категория {key}')
                    for task in value:
                        print(task)

        except FileNotFoundError as ex:
            print('Ошибка: не найден файл tasks.json в папке resources')

    @staticmethod
    def search_by_category() -> None:
        print('Введите категорию')
        category = input('-> ').strip()

        if not category:
            print('Ошибка: категория не может быть пустой')
            return

        try:
            tasks = Reader.search_by_category(category)

            if len(tasks) == 0:
                print(f'Задач с категорией {category} не найдено')
            else:
                print('Результат поиска:')
                for task in tasks:
                    print(task)

        except FileNotFoundError as ex:
            print('Ошибка: не найден файл tasks.json в папке resources')

    @staticmethod
    def search_by_key_word() -> None:
        print('Введите ключевое слово')
        word = input('-> ').strip()

        if not word:
            print('Ошибка: слово не может быть пустым')
            return

        try:
            tasks = Reader.search_key_word(word)

            if len(tasks) == 0:
                print(f'Задач с словом {word} не найдено')
            else:
                print('Результат поиска:')
                for task in tasks:
                    print(task)

        except FileNotFoundError as ex:
            print('Ошибка: не найден файл tasks.json в папке resources')

    @staticmethod
    def search_by_status() -> None:
        print('Выберите статус')
        print('(1) Выполнена')
        print('(2) Не выполнена')

        status = input('-> ').strip()

        if not status:
            print('Ошибка: статус не может быть пустым')
            return

        try:
            if int(status) < 1 or int(status) > 2:
                print('Ошибка: статус должен указываться числом 1 или 2')
                return
        except ValueError as ex:
            print('Ошибка: статус должен указываться числом 1 или 2')
            return

        try:
            tasks = Reader.search_by_status(int(status))

            if len(tasks) == 0:
                print(f'Задач со статусом {status} не найдено')
            else:
                print('Результат поиска:')
                for task in tasks:
                    print(task)

        except FileNotFoundError as ex:
            print('Ошибка: не найден файл tasks.json в папке resources')

    @staticmethod
    def update_status() -> None:
        print('Введите id задачи')
        id = input('-> ').strip()

        try:
            id = int(id)
            if id <= 0:
                print('Ошибка: id должен быть целым числом больше 0')
                return
        except ValueError as ex:
            print('Ошибка: id должен быть целым числом')
            return

        try:
            Writer.update_status(id)
            print('Задача успешно обновлена')
        except FileNotFoundError as ex:
            print('Ошибка: не найден файл tasks.json в папке resources')
        except TaskNotFoundError as ex:
            print(f'Ошибка: не найдена задача с id {id}')
        except IOError as ex:
            print('Ошибка: ошибка при записи в файл tasks.json')

    @staticmethod
    def update_task() -> None:
        print('Введите id задачи')
        id = input('-> ').strip()

        try:
            id = int(id)
            if id <= 0:
                print('Ошибка: id должен быть целым числом больше 0')
                return
        except ValueError as ex:
            print('Ошибка: id должен быть целым числом')
            return

        title = input('Введите новое название (или нажмите Enter, чтобы оставить без изменений) -> ').strip() or None
        description = input(
            'Введите новое описание (или нажмите Enter, чтобы оставить без изменений) -> ').strip() or None
        category = input(
            'Введите новую категорию (или нажмите Enter, чтобы оставить без изменений) -> ').strip() or None
        due_date = input('Введите новую дату (или нажмите Enter, чтобы оставить без изменений) -> ').strip() or None

        if due_date and not ProcessingOutput.is_valid_date(due_date):
            return

        print('Выберите новый приоритет (или нажмите Enter, чтобы оставить без изменений)')
        print('(1) Низкий')
        print('(2) Средний')
        print('(3) Высокий')

        priority_input = input('-> ').strip()
        priority = None
        if priority_input:
            try:
                if int(priority_input) < 1 or int(priority_input) > 3:
                    print('Ошибка: приоритет должен указываться числом 1, 2 или 3')
                    return
                priority = Priority.LOW if priority_input == '1' else Priority.MEDIUM \
                    if priority_input == '2' else Priority.HIGH
            except ValueError as ex:
                print('Ошибка: приоритет должен указываться числом 1, 2 или 3')
                return

        try:
            Writer.update_task(id, title, description, category, priority, due_date)
            print('Задача успешно обновлена')
        except FileNotFoundError as ex:
            print('Ошибка: не найден файл tasks.json в папке resources')
        except TaskNotFoundError as ex:
            print(f'Ошибка: не найдена задача с id {id}')
        except IOError as ex:
            print('Ошибка: ошибка при записи в файл tasks.json')

    @staticmethod
    def delete_by_id() -> None:
        print('Введите id задачи')
        id = input('-> ').strip()

        try:
            id = int(id)
            if id <= 0:
                print('Ошибка: id должен быть целым числом больше 0')
                return
        except ValueError as ex:
            print('Ошибка: id должен быть целым числом')
            return

        try:
            Writer.remove_task_by_id(id)
            print('Задача успешно удалена')
        except FileNotFoundError as ex:
            print('Ошибка: не найден файл tasks.json в папке resources')
        except TaskNotFoundError as ex:
            print(f'Ошибка: не найдена задача с id {id}')
        except IOError as ex:
            print('Ошибка: ошибка при записи в файл tasks.json')

    @staticmethod
    def delete_by_category() -> None:
        print('Введите категорию')
        print('Внимание: будут удалены ВСЕ задачи из введённое категории')

        category = input('-> ').strip()

        if not category:
            print('Ошибка: категория не может быть пустой')
            return

        try:
            Writer.remove_tasks_by_category(category)
            print(f'Задачи из категории {category} успешно удалены')
        except FileNotFoundError as ex:
            print('Ошибка: не найден файл tasks.json в папке resources')
        except TaskNotFoundError as ex:
            print(f'Ошибка: не найдены задача с категорией {category}')
        except IOError as ex:
            print('Ошибка: ошибка при записи в файл tasks.json')
