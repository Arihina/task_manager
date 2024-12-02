class ProcessingUserInput:
    @staticmethod
    def processing_get():
        pass

    @staticmethod
    def processing_search():
        pass

    @staticmethod
    def processing_add():
        pass

    @staticmethod
    def processing_update():
        pass

    @staticmethod
    def processing_delete():
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
                print('Неверный пункт меню')
