from manager.json_utilities import Reader


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
        pass

    @staticmethod
    def processing_update() -> None:
        pass

    @staticmethod
    def processing_delete() -> None:
        pass


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
