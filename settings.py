from tools.sqlSetting import set_user_name, add_user_to_access_group, delete_user_from_access_group, add_apps, get_apps_names_list, \
    get_access_apps_names_list_for_user, get_all_group_list
from inWorking.chatGPT.sqlChatGPT import set_bot_for_user
from tools.config.config import Config


class EasySettings:

    @staticmethod
    def run_function(func, arg=None):
        try:
            if arg is None:
                return func()
            else:
                return func(arg)
        except TypeError:
            print("Вы ошиблись с типом данных. Попробуйте ещё раз.")
            EasySettings.run_function(func, arg=None)
        except ValueError:
            print("Надо ввести целое число. Попробуйте ещё раз.")
            EasySettings.run_function(func, arg=None)

    @staticmethod
    def set_user_name():
        user_id = EasySettings.run_function(int, input("Введите user_id: "))
        user_name = input("Введите user_name: ")
        set_user_name(user_id=user_id, user_name=user_name)
        input("Нажмите Enter чтобы продолжить...")

    @staticmethod
    def add_access_rights():
        user_id = EasySettings.run_function(int, input("Введите user_id: "))
        group_list = get_all_group_list()
        print(group_list)

        group_name = input("Введите группу: ")
        if group_name in group_list:
            add_user_to_access_group(user_id=user_id, access_group_name=group_name)
        else:
            print(f"Нет группы доступа '{group_name}'")
        input("Нажмите Enter чтобы продолжить...")

    @staticmethod
    def delete_access_rights():
        user_id = EasySettings.run_function(int, input("Введите user_id: "))
        group_list = get_all_group_list()
        print(group_list)

        group_name = input("Введите группу: ")
        if group_name in group_list:
            delete_user_from_access_group(user_id=user_id, access_group_name=group_name)
        else:
            print(f"Нет группы доступа '{group_name}'")
        input("Нажмите Enter чтобы продолжить...")

    @staticmethod
    def add_app():
        app_name = input("Введите app_name: ")
        add_apps(app_name)
        input("Нажмите Enter чтобы продолжить...")

    @staticmethod
    def get_apps_names_list():
        print("Все приложения в таблице app: ")
        print(get_apps_names_list())
        input("Нажмите Enter чтобы продолжить...")

    @staticmethod
    def set_telegram_bot():
        new_token = input("Telegram token: ")
        Config().telegram.token = new_token
        input("Нажмите Enter чтобы продолжить...")

    @staticmethod
    def chat_gpt_makeCharacterBot_init():
        add_apps("chatGPT", "makeCharacterBot")
        input("Нажмите Enter чтобы продолжить...")

    @staticmethod
    def set_bot_for_user():
        user_id = EasySettings.run_function(int, input("Введите user_id: "))
        bot_name = input("Введите bot_name: ")
        set_bot_for_user(user_id=user_id, bot_name=bot_name)
        input("Нажмите Enter чтобы продолжить...")

    @staticmethod
    def run():
        print("\n")
        print("Выберете число нужного действия: ")
        print(
            "1. Изменить имя пользователя\n"
            "2. Добавить пользователя в группу доступа\n"
            "3. Удалить пользователя из группы доступа\n"
            "4. Добавить название приложения в базу данных\n"
            "5. Показать все приложения из базы данных\n"
            "6. Установить токен телеграма\n"
            "7. Проинициализировать chatGPT и makeCharacterBot\n"
            "8. Установить бота для юзера\n"
            "0. Выход\n"
        )
        choice = EasySettings.run_function(input, "Ваше число: ")
        match choice:
            case "1":
                EasySettings.set_user_name()
                EasySettings.run()
            case "2":
                EasySettings.add_access_rights()
                EasySettings.run()
            case "3":
                EasySettings.delete_access_rights()
                EasySettings.run()
            case "4":
                EasySettings.add_app()
                EasySettings.run()
            case "5":
                EasySettings.get_apps_names_list()
                EasySettings.run()
            case "6":
                EasySettings.set_telegram_bot()
                EasySettings.run()
            case "7":
                EasySettings.chat_gpt_makeCharacterBot_init()
                EasySettings.run()
            case "8":
                EasySettings.set_bot_for_user()
                EasySettings.run()
            case "0":
                exit(0)
            case _:
                print("\nВыберите из предложенного списка. ")
                input("Нажмите Enter чтобы продолжить...")
                EasySettings.run()


if __name__ == "__main__":
    EasySettings.run()
