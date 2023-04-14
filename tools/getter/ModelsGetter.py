from tools.config.config import Config
import os
from importlib import import_module
from platform import platform


def get_import_list():
    import_list = []
    app_root = os.walk('messenger')
    for root, dirs, files in app_root:
        if files is not None:
            for file in files:
                if file.endswith('.py') and file == "main.py":
                    import_list.append(".".join(root.split("\\" if is_windows_os() else "/")) + ".main")
    return import_list


def get_messenger_list():
    import_list = get_import_list()
    messenger_list = []
    for path in import_list:
        module = import_module(path)
        messenger_list.append(module.Messenger)
    return messenger_list


def is_windows_os():
    op_sys = platform().lower()
    if "window" in op_sys:
        return True
    else:
        return False


class ModelsGetter:
    """Возвращает модули в зависимости от конфига"""
    @staticmethod
    def messenger(messenger_name=None):
        if not messenger_name:
            config = Config()
            messenger_name = config.main_messenger

        messenger_list = get_messenger_list()
        index_count = -1
        for messenger in messenger_list:
            index_count += 1
            if messenger.name == messenger_name:
                return messenger_list[index_count]
        raise Exception("Нет такого мессенджера")



