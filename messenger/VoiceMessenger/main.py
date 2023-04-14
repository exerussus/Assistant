
from tools.interface import BaseMessenger


class Messenger(BaseMessenger):
    name = "VoiceMessenger"

    def __init__(self):
        pass

    def get_message(self) -> str:
        pass

    def response(self) -> None:
        pass

    def generate_answer(self) -> str:
        pass

    def access_denied(self, app_name: str) -> None:
        pass

    def input_message(self):
        pass
