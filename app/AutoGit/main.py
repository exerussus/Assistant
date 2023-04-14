
from tools.App import BaseApp


class App(BaseApp):
    name = "AutoGit"
    activate_words = ("/git",)  # Ключевые слова для активации
    assistant_type_accepted = ("TelegramAssistant",)  # Ассистенты, которые могут использовать данное приложение
    access = ("all", )  # Уровень доступа


