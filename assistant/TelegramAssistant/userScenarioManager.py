from tools.interface import UserScenarioManager
from tools.sqlSetting import get_access_rights, clean_user_status, get_user_status, set_user_status


class TelegramUserManager(UserScenarioManager):
    def get_user_scenario(self, user_id: int) -> (int, str, str, str):
        return get_user_status(user_id=user_id)

    def set_user_scenario(self, user_id: int, app_name: str, scenario: str):
        set_user_status(user_id=user_id, actually_app=app_name, scenario=scenario)

    def reset_user_scenario(self, user_id: int):
        clean_user_status(user_id=user_id)
