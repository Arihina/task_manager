import re
from datetime import datetime

from manager.exceptions.tasks_exceptions import TaskNotFoundError
from manager.json_utilities import Reader, Writer
from manager.models.priority import Priority
from manager.models.task import Task


class ProcessingOutput:
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

        if due_date and not ProcessingUserInput.is_valid_date(due_date):
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


class ProcessingUserInput:
    GET_MENU = {
        '1': ProcessingOutput.get_current,
        '2': ProcessingOutput.get_by_category
    }

    SEARCH_MENU = {
        '1': ProcessingOutput.search_by_category,
        '2': ProcessingOutput.search_by_status,
        '3': ProcessingOutput.search_by_key_word
    }

    UPDATE_MENU = {
        '1': ProcessingOutput.update_task,
        '2': ProcessingOutput.update_status
    }

    DELETE_MENU = {
        '1': ProcessingOutput.delete_by_id,
        '2': ProcessingOutput.delete_by_category
    }

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
    def processing_get() -> None:
        print('Просмотр задач')

        print("(1) Просмотр текущих")
        print("(2) Просмотр по категориям")

        choice = input('-> ')
        try:
            ProcessingUserInput.GET_MENU[choice]()
        except KeyError as ex:
            print('Ошибка: неверный пункт меню')

    @staticmethod
    def processing_search() -> None:
        print('Поиск задач по')

        print('(1) Категории')
        print('(2) Статусу')
        print('(3) Ключевому слову')

        choice = input('-> ')
        try:
            ProcessingUserInput.SEARCH_MENU[choice]()
        except KeyError as ex:
            print('Ошибка: неверный пункт меню')

    @staticmethod
    def processing_add() -> None:
        print('Добавить задачу')

        title = input('Введите название -> ').strip()
        if not title:
            print('Ошибка: название не может быть пустым')
            return

        description = input('Введите описание -> ').strip()
        if not description:
            print('Ошибка: описание не может быть пустым')
            return

        category = input('Введите категорию -> ').strip()
        if not category:
            print('Ошибка: категория не может быть пустой')
            return

        due_date = input('Введите дату -> ').strip()
        if not due_date:
            print('Ошибка: дата не может быть пустой')
            return
        if not ProcessingUserInput.is_valid_date(due_date):
            return

        print('Выберите приоритет')
        print('(1) Низкий')
        print('(2) Средний')
        print('(3) Высокий')

        priority = input('-> ').strip()
        if not priority:
            print('Ошибка: приоритет не может быть пустым')
            return
        try:
            if int(priority) < 1 or int(priority) > 3:
                print('Ошибка: приоритет должен указываться числом 1 или 3')
                return
        except ValueError as ex:
            print('Ошибка: приоритет должен указываться числом 1 или 3')
            return

        if priority == '1':
            priority = Priority.LOW
        elif priority == '2':
            priority = Priority.MEDIUM
        else:
            priority = Priority.HIGH

        try:
            Writer.add_task(Task(title, description, category, priority, due_date))
            print('Задача успешно добавлена')
        except FileNotFoundError as ex:
            print('Ошибка: не найден файл tasks.json в папке resources')

    @staticmethod
    def processing_update() -> None:
        print('Редактировать задачу')

        print('(1) Редактировать существующую')
        print('(2) Отметить выполненной')

        choice = input('-> ')
        try:
            ProcessingUserInput.UPDATE_MENU[choice]()
        except KeyError as ex:
            print('Ошибка: неверный пункт меню')

    @staticmethod
    def processing_delete() -> None:
        print('Удалить задачу')

        print('(1) По id')
        print('(2) По категории')

        choice = input('-> ')
        try:
            ProcessingUserInput.DELETE_MENU[choice]()
        except KeyError as ex:
            print('Ошибка: неверный пункт меню')


class App:
    MENU = {
        '1': ProcessingUserInput.processing_get,
        '2': ProcessingUserInput.processing_search,
        '3': ProcessingUserInput.processing_add,
        '4': ProcessingUserInput.processing_update,
        '5': ProcessingUserInput.processing_delete,
    }

    @staticmethod
    def print_main_menu() -> None:
        print('(1) Просмотреть')
        print('(2) Найти')
        print('(3) Добавить')
        print('(4) Изменить')
        print('(5) Удалить')
        print('(0) Выход')

    @staticmethod
    def run() -> None:
        print("Менеджер задач")

        while True:
            App.print_main_menu()
            choice = input('-> ')

            if choice == '0':
                print('Выход')
                break

            try:
                App.MENU[choice]()
            except KeyError as ex:
                print('Ошибка: неверный пункт меню')
