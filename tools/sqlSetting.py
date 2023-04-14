import sqlite3


class SettingsSql:

    def __init__(self):
        self.conn = sqlite3.connect("../data/settings.db" if __name__ == "__main__" else "data/settings.db")
        self.cur = self.conn.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, "
                         "name TEXT, "
                         "actually_app TEXT, "
                         "scenario TEXT)")

        self.cur.execute("CREATE TABLE IF NOT EXISTS user_access (user_id INTEGER, "
                         "app_name TEXT, "
                         "FOREIGN KEY (user_id) REFERENCES user(id),"
                         "FOREIGN KEY (app_name) REFERENCES app(name))")

        self.cur.execute("CREATE TABLE IF NOT EXISTS app (name TEXT PRIMARY KEY)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS admin_lsit (user_id INTEGER PRIMARY KEY)")

        self.cur.execute("CREATE TABLE IF NOT EXISTS tariff (user_id INTEGER PRIMARY KEY, "
                         "basic INTEGER, "
                         "standard INTEGER, "
                         "premium INTEGER)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS access_group (group_name TEXT PRIMARY KEY)")

    def add_all_apps(self, app_name_list: list[str]):
        for app_name in app_name_list:
            if not self.app_exist_check(app_name):
                self.add_app(app_name)

    def create_all_app_table_from_app(self):
        self.cur.execute("SELECT * FROM app")
        result = self.cur.fetchall()
        app_name_list = [x[0] for x in result]
        for app_name in app_name_list:
            self.create_app_table(app_name)

    def create_app_table(self, app_name: str):
        app_name_changed = "app_" + app_name
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {app_name_changed} (access_group TEXT PRIMARY KEY)")

    def add_new_access_group(self, access_group_name: str):
        self.cur.execute(f"SELECT group_name FROM access_group WHERE group_name='{access_group_name}'")
        result = self.cur.fetchone()
        if not result:
            self.cur.execute(f"INSERT INTO access_group (group_name) VALUES ('{access_group_name}')")
            self.conn.commit()

    def create_access_group_table(self, access_group_name: str):
        access_group_name_changed = "access_group_" + access_group_name
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {access_group_name_changed} (user_id INTEGER PRIMARY KEY)")
        self.conn.commit()

    def create_all_access_group_tables(self):
        self.cur.execute("SELECT * FROM access_group")
        result = self.cur.fetchall()
        access_group_list = [x[0] for x in result]
        for access_group in access_group_list:
            self.create_access_group_table(access_group)

    def add_user_to_access_group(self, user_id: int, access_group_name: str):
        access_group_name_changed = "access_group_" + access_group_name
        self.cur.execute(f"SELECT user_id FROM {access_group_name_changed} WHERE user_id='{user_id}'")
        result = self.cur.fetchone()
        if not result:
            self.cur.execute(f"INSERT INTO {access_group_name_changed} (user_id) VALUES ('{user_id}')")
            self.conn.commit()

    def delete_user_from_access_group(self, user_id: int, access_group_name: str):
        access_group_name_changed = "access_group_" + access_group_name
        self.cur.execute(f"DELETE FROM {access_group_name_changed} WHERE user_id='{user_id}'")
        self.conn.commit()

    def add_group_to_app_table(self, app_name: str, access_group_name: str):
        app_name_changed = "app_" + app_name
        self.cur.execute(f"SELECT access_group FROM {app_name_changed} WHERE access_group='{access_group_name}'")
        result = self.cur.fetchone()
        if not result:
            self.cur.execute(f"INSERT INTO {app_name_changed} (access_group) VALUES ('{access_group_name}')")
            self.conn.commit()

    def delete_group_from_app_table(self, app_name: str, access_group_name: str):
        app_name_changed = "app_" + app_name
        self.cur.execute(f"DELETE FROM {app_name_changed} WHERE access_group='{access_group_name}'")
        self.conn.commit()

    def get_access_groups_from_app(self, app_name: str):
        app_name_changed = "app_" + app_name
        self.cur.execute(f"SELECT * FROM {app_name_changed}")
        result = self.cur.fetchall()
        return [x[0] for x in result]

    def get_users_from_group(self, access_group_name: str):
        access_group_name_changed = "access_group_" + access_group_name
        self.cur.execute(f"SELECT * FROM {access_group_name_changed}")
        result = self.cur.fetchall()
        return [x[0] for x in result]

    def get_users_from_access_group(self, access_group_name: str):
        app_name_changed = "access_group_" + access_group_name
        self.cur.execute(f"SELECT * FROM {app_name_changed}")
        result = self.cur.fetchall()
        return [x[0] for x in result]

    def get_all_group_list(self):
        self.cur.execute("SELECT * FROM access_group")
        result = self.cur.fetchall()
        group_name_list = [x[0] for x in result]
        return group_name_list

    def get_admin_list(self):
        self.cur.execute("SELECT * FROM admin_lsit")
        result = self.cur.fetchall()
        return result

    def add_admin_rights(self, user_id: int):
        self.cur.execute(f"SELECT user_id FROM admin_lsit WHERE user_id='{user_id}'")
        result = self.cur.fetchone()
        if not result:
            query = f"INSERT INTO admin_lsit (user_id) VALUES ('{user_id}')"
            self.cur.execute(query)
            self.conn.commit()

    def delete_admin_rights(self, user_id: int):
        self.cur.execute("DELETE FROM admin_list WHERE user_id = ?", (user_id,))
        self.conn.commit()

    def admin_rights_check(self, user_id: int):
        self.cur.execute("SELECT * FROM admin_lsit WHERE user_id = ?", (user_id,))
        result = self.cur.fetchone()
        return True if result is not None else False

    def add_rights_for_free_app(self, user_id: int):
        """Выдает необходимые права новому пользователю"""

        from tools.getter.apps_getter import get_apps_list
        app_list = get_apps_list()
        accessed_apps = []
        for app in app_list:
            print(f"app = {app}")
            if app.access == "all" and app.name != "app_name":
                print(f"app,name = {app.name}")
                accessed_apps.append(app.name)
        for app_name in accessed_apps:
            self.add_access_rights(user_id=user_id, app_name=app_name)

    def get_user_tariff(self, user_id: int):
        """"""
        def execute():
            self.cur.execute(f"SELECT * FROM tariff WHERE user_id = {user_id}")
            return self.cur.fetchone()

        result = execute()
        if result is None:
            self.add_user_data_to_tariff(user_id=user_id)
            result = execute()

        user_tariff_info = {'user_id': user_id,
                            'basic': result[1],
                            'standard': result[2],
                            'premium': result[3], }
        return user_tariff_info

    def add_user_data_to_tariff(self, user_id: int, basic=0, standard=0, premium=0):
        query = f"INSERT INTO tariff (user_id, basic, standard, premium) VALUES ({user_id}, {basic}, {standard}, {premium})"
        self.cur.execute(query)
        self.conn.commit()

    def add_days_for_user_tariff(self, user_id: int, basic: int, standard: int, premium: int):

        result = self.get_user_tariff(user_id=user_id)
        basic += result['basic']
        standard += result['standard']
        premium += result['premium']
        self.set_days_to_tariff_plan_for_user(user_id=user_id,
                                              basic=basic,
                                              standard=standard,
                                              premium=premium)

    def set_days_to_tariff_plan_for_user(self, user_id: int, basic: int, standard: int, premium: int):
        query = f"UPDATE tariff SET  user_id = {user_id}, " \
                f"basic = {basic}, " \
                f"standard = {standard}, " \
                f"premium = {premium} " \
                f"WHERE user_id = {user_id}"
        self.cur.execute(query)
        self.conn.commit()

    def get_apps_names_list(self):
        self.cur.execute("SELECT * FROM app")
        return self.cur.fetchall()

    def execute(self, user_id):
        self.cur.execute("SELECT * FROM user WHERE id = ?", (user_id,))
        return self.cur.fetchone()

    def set_user_name(self, user_id: int, user_name: str):
        result = user_name, user_id
        self.cur.execute("UPDATE user SET name = ? WHERE id = ?", result)
        self.conn.commit()

    def get_user_status(self, user_id: int):
        result = self.execute(user_id)
        if self.execute(user_id) is None:
            result = (user_id, '', '', '')
            self.cur.execute("INSERT INTO user VALUES (?, ?, ?, ?)", result)
            self.add_user_to_access_group(user_id, "all")
            self.conn.commit()
            self.add_rights_for_free_app(user_id)
        return result

    def set_user_status(self, user_id: int, actually_app: str, scenario: str):
        result = actually_app, scenario, user_id,
        self.cur.execute("UPDATE user SET actually_app = ?, scenario = ? WHERE id = ?", result)
        self.conn.commit()

    def delete_access_rights(self, user_id: int, app_name: str):
        result = user_id, app_name
        self.cur.execute("DELETE FROM user_access WHERE user_id = ? AND app_name = ?", result)
        self.conn.commit()

    def add_access_rights(self, user_id: int, app_name: str):
        self.cur.execute("SELECT * FROM user_access WHERE user_id = ? AND app_name = ?", (user_id, app_name))
        rights_exist = self.cur.fetchone()
        if rights_exist is None:
            self.cur.execute("INSERT INTO user_access VALUES (?, ?)", (user_id, app_name))
            self.conn.commit()

    def get_access_rights(self, user_id: int, app_name: str):
        result = (user_id, app_name)
        self.cur.execute("SELECT * FROM user_access WHERE user_id = ? AND app_name = ?", result)
        rights = self.cur.fetchone()
        return True if rights is not None else False

    def add_app(self, app_name: str):
        self.cur.execute("INSERT INTO app VALUES (?)", (app_name,))
        self.conn.commit()

    def app_exist_check(self, app_name: str):
        self.cur.execute("SELECT * FROM app WHERE name = ? ", (app_name,))
        result = self.cur.fetchone()
        return True if result is not None else False

    def get_all_user_access_rights(self, user_id: int):

        self.cur.execute("SELECT app_name FROM user_access WHERE user_id = ?", (user_id,))
        app_names = self.cur.fetchall()
        return app_names


def get_access_apps_names_list_for_user(user_id: int):
    _classExemplar = SettingsSql()
    app_names = _classExemplar.get_all_user_access_rights(user_id=user_id)
    _classExemplar.conn.close()
    return app_names


def get_apps_names_list():
    _classExemplar = SettingsSql()
    apps_names_list = _classExemplar.get_apps_names_list()
    _classExemplar.conn.close()
    apps_names_tuple = tuple([x[0] for x in apps_names_list])
    return apps_names_tuple


def get_user_status(user_id: int):
    """Возвращает словарь с ключами: id, user_name, activated_app, scenario."""
    _classExemplar = SettingsSql()
    result = _classExemplar.get_user_status(user_id=user_id)
    dict_result = {"id": result[0], 'user_name': result[1], "activated_app": result[2], "scenario": result[3]}
    _classExemplar.conn.close()
    return dict_result


def set_user_status(user_id: int, actually_app: str, scenario: str):
    _classExemplar = SettingsSql()
    _classExemplar.set_user_status(user_id=user_id, actually_app=actually_app, scenario=scenario)
    _classExemplar.conn.close()


def add_access_rights(user_id: int, app_name: str):
    _classExemplar = SettingsSql()
    _classExemplar.add_access_rights(user_id=user_id, app_name=app_name)
    _classExemplar.conn.close()


def delete_access_rights(user_id: int, app_name: str):
    _classExemplar = SettingsSql()
    _classExemplar.delete_access_rights(user_id=user_id, app_name=app_name)
    _classExemplar.conn.close()


def get_access_rights(user_id: int, app_name: str):
    _classExemplar = SettingsSql()
    group_list = _classExemplar.get_access_groups_from_app(app_name)
    user_id_set = set()
    for access_group in group_list:
        user_list = _classExemplar.get_users_from_group(access_group)
        for user_id in user_list:
            user_id_set.add(user_id)
    if user_id in user_id_set:
        return True
    else:
        return False

def set_user_name(user_id: int, user_name: str):
    _classExemplar = SettingsSql()
    _classExemplar.set_user_name(user_id=user_id, user_name=user_name)
    _classExemplar.conn.close()


def clean_user_status(user_id: int):
    actually_app = scenario = ""
    set_user_status(user_id=user_id, actually_app=actually_app, scenario=scenario)


def add_apps(*apps_names: str):
    _classExemplar = SettingsSql()
    for app_name in apps_names:
        if not _classExemplar.app_exist_check(app_name=app_name):
            _classExemplar.add_app(app_name=app_name)
    _classExemplar.conn.close()


def get_user_tariff(user_id: int):
    """Возвращает словать с количеством оплаченных дней каждого тарифа: 'basic', 'standard', 'premium'"""
    _classExemplar = SettingsSql()
    user_tariff = _classExemplar.get_user_tariff(user_id=user_id)
    _classExemplar.conn.close()
    return user_tariff


def add_admin_rights(user_id: int):
    """Даёт админку пользователю"""
    _classExemplar = SettingsSql()
    _classExemplar.add_admin_rights(user_id=user_id)
    _classExemplar.conn.close()


def delete_admin_rights(user_id: int):
    """Удаляет админку пользователя"""
    _classExemplar = SettingsSql()
    _classExemplar.delete_admin_rights(user_id=user_id)
    _classExemplar.conn.close()


def admin_rights_check(user_id: int):
    """Возвращает True, если пользователь админ"""
    _classExemplar = SettingsSql()
    is_admin = _classExemplar.admin_rights_check(user_id=user_id)
    _classExemplar.conn.close()
    return is_admin


def get_admin_list():
    """Возвращает tuple user_id всех админов"""
    _classExemplar = SettingsSql()
    admin_list = _classExemplar.get_admin_list()
    _classExemplar.conn.close()
    admin_tuple = tuple([x[0] for x in admin_list])
    return admin_tuple


def create_all_app_table_from_app():
    """Создает таблицы доступа для всех приложений"""
    _classExemplar = SettingsSql()
    _classExemplar.create_all_app_table_from_app()
    _classExemplar.conn.close()


def add_group_to_app_table(app_name: str, access_group_name: str):
    """Добавляет права группе пользователей использовать приложение"""
    _classExemplar = SettingsSql()
    _classExemplar.add_group_to_app_table(app_name=app_name, access_group_name=access_group_name)
    _classExemplar.conn.close()


def create_access_group_table(access_group_name: str):
    """Создает группу доступа пользователей"""
    _classExemplar = SettingsSql()
    _classExemplar.add_new_access_group(access_group_name=access_group_name)
    _classExemplar.create_access_group_table(access_group_name=access_group_name)
    _classExemplar.conn.close()


def add_new_access_group(access_group_name: str):
    """Добавляет группу доступа"""
    _classExemplar = SettingsSql()
    _classExemplar.add_new_access_group(access_group_name=access_group_name)
    _classExemplar.conn.close()


def create_all_access_group_tables():
    """Создает все таблицы группы доступа пользователей"""
    _classExemplar = SettingsSql()
    _classExemplar.create_all_access_group_tables()
    _classExemplar.conn.close()


def add_user_to_access_group(user_id: int, access_group_name: str):
    """Добавляет пользователя в группу доступа"""
    _classExemplar = SettingsSql()
    _classExemplar.add_user_to_access_group(user_id=user_id, access_group_name=access_group_name)
    _classExemplar.conn.close()


def delete_user_from_access_group(user_id: int, access_group_name: str):
    """Удаляет пользователя из группы доступа"""
    _classExemplar = SettingsSql()
    _classExemplar.delete_user_from_access_group(user_id=user_id, access_group_name=access_group_name)
    _classExemplar.conn.close()


def get_all_group_list():
    """Возвращает все группы доступа пользователей"""
    _classExemplar = SettingsSql()
    return _classExemplar.get_all_group_list()


def initialization():
    from tools.getter.apps_getter import get_apps_list

    def default_access_groups():
        groups = ('all', 'admin', 'private')
        for i in groups:
            add_new_access_group(i)

    def add_all_apps(app_list: list):
        for app in app_list:
            add_apps(app.name)

    def add_access_to_admins():
        app_list = get_apps_list()
        admin = "admin"
        for app in app_list:
            app_name = app.name
            add_group_to_app_table(app_name=app_name, access_group_name=admin)

    def set_access_control_to_app(app_list: list):
        for app in app_list:
            for group in app.access:
                add_group_to_app_table(app_name=app.name, access_group_name=group)

    _app_list = get_apps_list()
    add_all_apps(_app_list)
    default_access_groups()
    create_all_app_table_from_app()
    set_access_control_to_app(_app_list)
    create_all_access_group_tables()
    add_access_to_admins()


if __name__ == "__main__":

    add_admin_rights(1557628538)
