from tools.getter.apps_getter import get_apps_list


class AppList:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = get_apps_list()
        return cls.instance
