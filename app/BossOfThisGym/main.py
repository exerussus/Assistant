
from tools.App import BaseApp


class App(BaseApp):
    name = "BossOfThisGym"
    activate_words = ("/git",)
    assistant_type_accepted = ("TelegramAssistant",)
    access = ("admin", )
