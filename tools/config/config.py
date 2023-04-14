
from pydantic import BaseModel


class BaseMessenger(BaseModel):
    name: str


class BaseAssistant(BaseModel):
    name: str


class TelegramBot(BaseModel):
    name: str
    token: str


class TelegramConfig(BaseModel):
    messenger_name: str
    token: str
    bot_list: list[TelegramBot]

    def add_bot(self, bot_name: str, bot_token: str):
        no_repeats = True
        index_count = -1
        for bot in self.bot_list:
            index_count += 1
            if bot_name == bot.name:
                self.bot_list[index_count].token = bot_token
                no_repeats = False
                break
        if no_repeats:
            self.bot_list.append(TelegramBot.parse_raw('{"name": "' + bot_name + '", "token": "' + bot_token + '"}'))

    def delete_bot(self, bot_name: str):
        index_count = -1
        for bot in self.bot_list:
            index_count += 1
            if bot.name == bot_name:
                self.bot_list.pop(index_count)
                break


class OpenAI(BaseModel):
    token: str


class Container(BaseModel):
    main_assistant: str
    main_messenger: str
    assistant_list: list[BaseAssistant]
    messenger_list: list[BaseMessenger]
    telegram: TelegramConfig
    openai: OpenAI

    @staticmethod
    def get_config_json():
        with open('../data/config.json' if __name__ == "__main__" else 'data/config.json', "r") as f:
            return f.read()

    def save(self):
        jsn = self.json()
        with open('../data/config.json' if __name__ == "__main__" else 'data/config.json', "w") as f:
            f.write(jsn)

    @staticmethod
    def reset():
        standard_settings = """
        {   
            "main_assistant": "TelegramAssistant",
            "main_messenger": "TelegramMessenger",
            "assistant_list": [{"name": "TelegramAssistant"}, {"name": "VoiceAssistant"}],
            "messenger_list": [{"name": "TelegramMessenger"}, {"name": "VoiceMessenger"}],
            "telegram": {"messenger_name": "TelegramMessenger", "token": "", "bot_list": []},
            "openai": {"token": ""}
        }
        """
        _config = Container.parse_raw(standard_settings)
        _config.save()


class Config:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = Container.parse_raw(Container.get_config_json())
        return cls.instance


def initialization():
    Container.reset()


if __name__ == '__main__':
    # reset()
    config = Config()
    print(config.telegram.messenger_name)

    




