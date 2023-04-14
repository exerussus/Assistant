from tools.sqlSetting import initialization as sql_setting_init
from tools.config.config import initialization as config_init


def initialization():
    sql_setting_init()
    config_init()


if __name__ == '__main__':
    initialization()
