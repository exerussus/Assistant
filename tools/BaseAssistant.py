from tools.interface import BaseMessenger, AppManager, UserScenarioManager
from tools.ScenarioInspector import ScenarioInspector
from tools.getter.apps_getter import get_app
from abc import abstractmethod
from datetime import datetime


class BaseAssistant:

    def __init__(self,
                 messenger: BaseMessenger,
                 app_manager: AppManager,
                 user_scenario_manager: UserScenarioManager,
                 scenario_inspector: ScenarioInspector):
        self.messanger = messenger
        self.app_manager = app_manager
        self.user_scenario_manager = user_scenario_manager
        self.scenario_inspector = scenario_inspector

    @abstractmethod
    def logger(self, user_id: int, message: str, first_name="Anon"):
        """Shows the message data in the console \n
        Показывает данные сообщения из телеграмма в консоли"""
        pass

    @abstractmethod
    def poling_get_message(self):
        """Отслеживает сигнал от пользователя и запускает request_processing"""
        pass

    def request_processing(self, user_id: int, message: str):
        user_message = message
        user_scenario = self.user_scenario_manager.get_user_scenario(user_id=user_id)
        app_list = self.app_manager.app_list()
        activated_app = self.scenario_inspector.is_activated_app(user_scenario=user_scenario)

        # Проверяем, есть ли активное приложение у пользователя
        if not activated_app:
            # Получаем имя приложения для запуска
            app_name = self.scenario_inspector.identify_application(message=user_message, app_list=app_list)

            if self.app_manager.get_access_to_app(user_id=user_id, app_name=app_name):
                app = get_app(app_name)
                if self.app_manager.app_type_accepted(app):
                    self.app_manager.app_run(user_id=user_id,
                                             app=app,
                                             message=user_message,
                                             messenger=self.messanger,
                                             user_scenario_manager=self.user_scenario_manager,
                                             app_name=app.name)

        else:
            app = get_app(activated_app)
            # Запуск приложения по сценарию
            self.app_manager.app_run(user_id=user_id,
                                     app=app,
                                     message=user_message,
                                     messenger=self.messanger,
                                     user_scenario_manager=self.user_scenario_manager,
                                     app_name=app.name)


