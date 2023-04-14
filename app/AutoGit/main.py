
from tools.App import BaseApp


class App(BaseApp):
    name = "AutoGit"
    activate_words = ("/git",)
    assistant_type_accepted = ("TelegramAssistant",)
    access = ("admin", )
