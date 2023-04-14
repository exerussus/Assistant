from typing import Any
from tools.getter.app_list import AppList
from tools.interface import AppManager, BaseMessenger, UserScenarioManager
from tools.sqlSetting import get_access_rights as user_has_access
from tools.config.config import Config


class TelegramAppManager(AppManager):

    def app_type_accepted(self, app: Any):
        if Config().main_assistant in app.assistant_type_accepted:
            return True
        else:
            return False

    def app_list(self) -> (Any, Any):
        return AppList()

    def app_run(self,
                user_id: int,
                app: Any,
                message: str,
                messenger: BaseMessenger,
                user_scenario_manager: UserScenarioManager,
                app_name: str) -> None:
        accepted = user_has_access(user_id=user_id, app_name=app.name)
        if accepted:
            app.command_run(user_id, message, user_scenario_manager, messenger, app_name)

        else:
            messenger.response(user_id, "У вас нет прав на использование данной команды.")
            user_scenario_manager.reset_user_scenario(user_id=user_id)

    def get_access_to_app(self, user_id: int, app_name: str) -> bool:
        return user_has_access(user_id=user_id, app_name=app_name)
