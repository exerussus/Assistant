from tools.interface import UserScenarioManager, BaseMessenger
from abc import abstractmethod
from tools.debugger.debuger import debug_log


class BaseApp:

    name = ""
    activate_words: tuple[str]
    assistant_type_accepted: tuple[str]
    access: tuple[str]

    def __init__(self,
                 user_id: int,
                 message: str,
                 user_scenario_manager: UserScenarioManager,
                 messenger: BaseMessenger,
                 app_name: str):
        self.user_id = user_id
        self.user_scenario_manager = user_scenario_manager
        self.messenger = messenger
        self.actually_status = self.user_scenario_manager.get_user_scenario(self.user_id)
        self.app_name = app_name
        self.debug_mode = True
        self.message = message

    def run(self):
        """Запускает метод в зависимости от текущего сценария. В начале всегда срабатывает beginning, а затем
        выбранный в beginning последующий сценарий. Сценарии можно переименовывать и расширять."""
        import os
        from importlib import import_module
        from platform import platform

        def is_windows_os():
            op_sys = platform().lower()
            if "window" in op_sys:
                return True
            else:
                return False

        import_list = []
        app_root = os.walk(f'app\\{self.app_name}\\scenario')
        for root, dirs, files in app_root:
            if files is not None:
                for file in files:
                    if file.endswith('.py'):
                        x = "\\" if is_windows_os() else "/"
                        import_list.append(".".join(root.split(x)) + "." + file[:-3])
        scenario_list = []
        for path in import_list:
            module = import_module(path)
            scenario_list.append(module.Scenario)
        for scenario in scenario_list:
            if scenario.name == self.actually_status["scenario"]:
                scenario(user_id=self.user_id,
                         message=self.message,
                         user_scenario_manager=self.user_scenario_manager,
                         messenger=self.messenger,
                         app_name=self.app_name).run()

    @staticmethod
    def command_run(user_id: int,
                    message: str,
                    user_scenario_manager: UserScenarioManager,
                    messenger: BaseMessenger,
                    app_name: str):
        """Обязательная функция. Название менять нельзя, так как её вызывает handler."""

        _classExemplar = BaseApp(
                                user_id=user_id,
                                message=message,
                                user_scenario_manager=user_scenario_manager,
                                messenger=messenger,
                                app_name=app_name)
        _classExemplar.run()


class BaseScenario:
    name: str

    def __init__(self,
                 user_id: int,
                 message: str,
                 user_scenario_manager: UserScenarioManager,
                 messenger: BaseMessenger,
                 app_name: str):
        self.user_id = user_id
        self.user_scenario_manager = user_scenario_manager
        self.messenger = messenger
        self.actually_status = self.user_scenario_manager.get_user_scenario(self.user_id)
        self.debug_mode = True
        self.message = message
        self.app_name = app_name

    def debug_log(self, debug_mode,
                  text: str = "",
                  scenario_start: str = "",
                  condition: str = "",
                  color: str = "blue"):
        """Выводит логи в консоль."""
        debug_log(app_name=self.app_name,
                  debug_mode=debug_mode,
                  message=text,
                  scenario_start=scenario_start,
                  condition=condition,
                  color=color)

    def send_message(self, text: str, user_id=None):
        """Посылает сообщение пользователю. По-умолчанию user_id = self.user_id"""
        self.debug_log(self.debug_mode, text=text)
        if user_id is None:
            self.messenger.response(user_id=self.user_id, message=text)
        else:
            self.messenger.response(user_id=user_id, message=text)

    def set_status(self, scenario: str, activated_app=None):
        """Меняет активный скрипт и сценарий. По-умолчанию ставит активный скрипт как self.app_name."""
        if activated_app is None:
            self.user_scenario_manager.set_user_scenario(user_id=self.user_id, app_name=self.app_name,
                                                         scenario=scenario)
        else:
            self.user_scenario_manager.set_user_scenario(user_id=self.user_id, app_name=activated_app,
                                                         scenario=scenario)

    def reset_status(self):
        self.user_scenario_manager.set_user_scenario(user_id=self.user_id, app_name="", scenario="")

    def run(self):
        self.do(user_id=self.user_id,
                message=self.message,
                user_scenario_manager=self.user_scenario_manager,
                messenger=self.messenger)

    @abstractmethod
    def do(self,
            user_id: int,
            message: str,
            user_scenario_manager: UserScenarioManager,
            messenger: BaseMessenger):
        pass


    # @staticmethod
    # def run(
    #          user_id: int,
    #          message: str,
    #          user_scenario_manager: UserScenarioManager,
    #          messenger: BaseMessenger,
    #          app_name: str):
    #     _scenario = BaseScenario(user_id=user_id,
    #                              message=message,
    #                              user_scenario_manager=user_scenario_manager,
    #                              messenger=messenger,
    #                              app_name=app_name)
    #     _scenario.do(user_id=user_id,
    #                  message=message,
    #                  user_scenario_manager=user_scenario_manager,
    #                  messenger=messenger)
