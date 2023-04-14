from tools.App import BaseScenario
from tools.interface import UserScenarioManager, BaseMessenger
from telebot import types
from assistant.TelegramAssistant.bot import Bot


class Scenario(BaseScenario):
    name = ""
    app_name = "BossOfThisGym"

    def do(self,
           user_id: int,
           message: str,
           user_scenario_manager: UserScenarioManager,
           messenger: BaseMessenger):
        pass



