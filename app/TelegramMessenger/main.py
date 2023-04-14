
from tools.App import BaseApp


class App(BaseApp):
    name = "TelegramMessenger"
    activate_words = ()  # Ключевые слова для активации
    assistant_type_accepted = ("TelegramAssistant",)  # Ассистенты, которые могут использовать данное приложение
    access = ("all", )  # Уровень доступа


