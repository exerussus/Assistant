from tools.App import BaseScenario
from tools.interface import UserScenarioManager, BaseMessenger
from telebot import types
from assistant.TelegramAssistant.bot import Bot


class Scenario(BaseScenario):
    name = ""
    app_name = "AutoGit"

    def do(self,
           user_id: int,
           message: str,
           user_scenario_manager: UserScenarioManager,
           messenger: BaseMessenger):

        scenario_start = "choice"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Скачать на пк")
        btn2 = types.KeyboardButton("Загрузить в облако")
        markup.add(btn1, btn2)
        Bot().send_message(self.user_id, text="Выберите действие: ", reply_markup=markup)
        self.debug_log(self.debug_mode, scenario_start=scenario_start, text="Начало команды", color="blue")
        self.set_status(scenario=scenario_start)

