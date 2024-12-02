from manager.json_utilities import Writer
from manager.models.priority import Priority
from manager.models.task import Task
from manager.processing.output import ProcessingOutput


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
        if not ProcessingOutput.is_valid_date(due_date):
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
