from tools.BaseAssistant import BaseAssistant, BaseMessenger, AppManager, UserScenarioManager, ScenarioInspector
from datetime import datetime
from tools.debugger.debuger import debug_log
from requests.exceptions import ReadTimeout
from tools.config.config import Config
from tools.getter.ModelsGetter import ModelsGetter
from assistant.TelegramAssistant.bot import Bot
from assistant.TelegramAssistant.telegramAppManager import TelegramAppManager
from assistant.TelegramAssistant.userScenarioManager import TelegramUserManager
from tools.ScenarioInspector import ScenarioInspector
import telebot


def do_func(function, arg1=None, arg2=None, arg3=None, arg4=None):
    try:
        if arg1 is None:
            function()
        elif arg2 is None:
            function(arg1)
        elif arg3 is None:
            function(arg1, arg2)
        elif arg4 is None:
            function(arg1, arg2, arg3)
        else:
            function(arg1, arg2, arg3, arg4)

    except ReadTimeout:
        debug_log(debug_mode=True, comment="Нет соединения с интернетом...", color="red")


class Assistant(BaseAssistant):

    def logger(self, user_id: int, message: str, first_name="Anon"):
        """Shows the message data in the console \n
        Показывает данные сообщения из телеграмма в консоли"""

        # get_user_status(_message.from_user.id)["user_name"]
        name = self.user_scenario_manager.get_user_scenario(user_id)["user_name"]
        if name is None:
            name = first_name
        debug_log(debug_mode=True, user_id=user_id, message=message, user_name=name)

    def poling_get_message(self):

        bot = Bot()

        @bot.message_handler(content_types=['text'])
        def get_text_messages(message):
            message_time = datetime.utcfromtimestamp(message.date)
            now = datetime.utcnow()
            delta = now - message_time
            user_id = message.from_user.id

            if delta.total_seconds() < 40:
                do_func(self.logger, arg1=user_id, arg2=message.text, arg3=message.from_user.first_name)

                self.request_processing(user_id=user_id, message=message.text)

        bot.polling(none_stop=True, interval=0)


def run():
    assistant = Assistant(
        user_scenario_manager=TelegramUserManager(),
        app_manager=TelegramAppManager(),
        messenger=ModelsGetter.messenger(Config().telegram.messenger_name)(),
        scenario_inspector=ScenarioInspector())

    assistant.poling_get_message()


if __name__ == '__main__':
    run()
    