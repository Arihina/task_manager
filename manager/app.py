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
        print('Введите категорию')
        category = input('-> ').strip()

        if not category:
            print('Ошибка: категория не может быть пустой')
            return

        try:
            tasks = Reader.get_tasks_by_category(category)

            if len(tasks) == 0:
                print('Нет задач в данной категории')
            else:
                print(f'Задачи в категории {category}')
                for task in tasks:
                    print(task)
        except FileNotFoundError as ex:
            print('Ошибка: не найден файл tasks.json в папке resources')


class ProcessingUserInput:
    GET_MENU = {
        '1': ProcessingOutput.get_current,
        '2': ProcessingOutput.get_by_category
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
        pass

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
