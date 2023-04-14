
from tools.config.config import Config
from tools.interface import BaseScenarioInspector
from typing import Any


class ScenarioInspector(BaseScenarioInspector):

    def identify_application(self, message: str, app_list: (Any, Any)) -> str or None:
        for app in app_list:
            if message in app.activate_words:
                return app.name

        return Config().main_messenger

    def is_activated_app(self, user_scenario: (int, str, str, str)) -> str or None:
        activated_app = user_scenario["activated_app"]

        if activated_app:
            return activated_app
        else:
            return None
