
from tools.interface import BaseMessenger
from assistant.TelegramAssistant.bot import Bot


class Messenger(BaseMessenger):
    name = "TelegramMessenger"

    def __init__(self):
        self.bot = Bot()

    def response(self, user_id: int, message: str) -> None:
        self.bot.send_message(user_id, text=message)

    def access_denied(self, user_id: int) -> None:
        self.bot.send_message(user_id, text="У вас нет прав использования чат-бота.")
