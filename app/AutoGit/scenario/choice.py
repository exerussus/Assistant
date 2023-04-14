from tools.App import BaseScenario
from tools.interface import UserScenarioManager, BaseMessenger
from telebot import types
from app.AutoGit import run as git
from assistant.TelegramAssistant.bot import Bot


class Scenario(BaseScenario):
    name = ""
    app_name = "AutoGit"

    def do(self,
           user_id: int,
           message: str,
           user_scenario_manager: UserScenarioManager,
           messenger: BaseMessenger):

        match self.message.text:

            case "Скачать на пк":
                git.pull()
                self.reset_status()
                Bot().send_message(self.user_id, "Готово.", reply_markup=types.ReplyKeyboardRemove())
            case "Загрузить в облако":
                git.push()
                self.reset_status()
                Bot().send_message(self.user_id, "Готово.", reply_markup=types.ReplyKeyboardRemove())
            case "Создать первый коммит":
                git.init()
                self.reset_status()
                Bot().send_message(self.user_id, "Готово.", reply_markup=types.ReplyKeyboardRemove())
            case _:
                Bot().send_message(self.user_id, "Некорректная команда. Выход из функции.", reply_markup=types.ReplyKeyboardRemove())
                self.reset_status()

