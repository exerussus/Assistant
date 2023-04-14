import telebot
from tools.config.config import Config


class Bot:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = telebot.TeleBot(Config().telegram.token)
        return cls.instance
