from tools.App import BaseScenario
from tools.interface import UserScenarioManager, BaseMessenger


class Scenario(BaseScenario):
    name = ""
    app_name = "TelegramMessenger"

    def do(self,
           user_id: int,
           message: str,
           user_scenario_manager: UserScenarioManager,
           messenger: BaseMessenger):

        self.send_message("Выберите дату")
        self.user_scenario_manager.set_user_scenario(user_id=self.user_id, scenario="", app_name=self.app_name)

