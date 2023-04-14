import os
from importlib import import_module
from platform import platform


def get_import_list():
    import_list = []
    app_root = os.walk('app')
    for root, dirs, files in app_root:
        if files is not None:
            for file in files:
                if file.endswith('.py') and file == "main.py":
                    import_list.append(".".join(root.split("\\" if is_windows_os() else "/")) + ".main")
    return import_list


def get_apps_list():
    import_list = get_import_list()
    apps_list = []
    for path in import_list:
        module = import_module(path)
        apps_list.append(module.App)
    return apps_list


def get_app(app_name: str):
    module = import_module(f"app.{app_name}.main")
    return module.App


def is_windows_os():
    op_sys = platform().lower()
    if "window" in op_sys:
        return True
    else:
        return False


