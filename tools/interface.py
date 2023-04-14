from abc import abstractmethod, abstractproperty
from typing import Any


class BaseMessenger:

    name: str
    __last_message: str

    @abstractmethod
    def response(self, user_id: int, message: str) -> None:
        """Отправляет сообщение от ассистента"""
        pass

    @abstractmethod
    def access_denied(self, user_id: int) -> None:
        """Оповещает пользователя о том, что у него недостаточно прав для использования приложения app_name"""
        pass

    @property
    def last_message(self):
        return BaseMessenger.__last_message

    @last_message.setter
    def last_message(self, message: str):
        BaseMessenger.__last_message = message


class UserScenarioManager:

    @abstractmethod
    def get_user_scenario(self, user_id: int) -> (int, str, str, str):
        """Возвращает активный сценарий пользователя в виде dict:
            {id: int, user_name: str, activated_app: str, scenario: str}

            Если данного пользователя нет - создает его.
            """
        pass

    @abstractmethod
    def set_user_scenario(self, user_id: int, app_name: str, scenario: str):
        """Устанавливает активный сценарий у пользователя"""
        pass

    @abstractmethod
    def reset_user_scenario(self, user_id: int):
        """Сбрасывает активный сценарий у пользователя"""
        pass


class AppManager:

    @abstractmethod
    def app_list(self) -> (Any, Any):
        """Возвращает список приложений"""
        pass

    @abstractmethod
    def app_run(self,
                user_id: int,
                app: Any,
                message: str,
                messenger: BaseMessenger,
                user_scenario_manager: UserScenarioManager,
                app_name: str) -> None:
        """Запускает приложение с именем app_name для пользователя user_id"""
        pass

    @abstractmethod
    def app_type_accepted(self, app: Any):
        """Возвращает допустимость использования приложения данным ассистентом"""
        pass

    @abstractmethod
    def get_access_to_app(self, user_id: int, app_name: str) -> bool:
        """Проверяет наличие прав пользователя на использование приложения"""
        pass


class BaseScenarioInspector:

    @abstractmethod
    def is_activated_app(self, user_scenario: (int, str, str, str)) -> str or None:
        """Проверяет наличие активного приложения у пользователя. Возвращает название активного приложения и сценарий"""
        pass

    @abstractmethod
    def identify_application(self, message: str, app_list: (Any, Any)) -> str:
        """Возвращает имя приложения для запуска"""
        pass

