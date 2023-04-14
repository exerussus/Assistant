
from datetime import datetime
from colorama import init, Fore
init(autoreset=True)


def debug_log(debug_mode=True,
              pref="",
              app_name="",
              comment="",
              variable="",
              scenario_start="",
              scenario_end="",
              condition="",
              color="green",
              user_id="",
              user_name="",
              message=""):
    """Печатает логи различных состояний в нужном цвете. Принимает аргументы:

              pref - Префикс
              debug_mode - включение/выключение функции;
              app_name - имя приложения;
              text - комментарий;
              variable - значение переменной, лучше записывать как: f{x=};
              scenario_start - запускающийся сценарий;
              scenario_end - завершающийся сценарий;
              condition - условие в завершающемся сценарии;
              color - цвет текста (white, blue, red, green, yellow).
              """
    if debug_mode:
        match color:
            case "white":
                text_color = Fore.WHITE
            case "blue":
                text_color = Fore.BLUE
            case "red":
                text_color = Fore.RED
            case "green":
                text_color = Fore.GREEN
            case "yellow":
                text_color = Fore.YELLOW
            case _:
                text_color = Fore.RESET

        time = datetime.now()
        time_now = time.strftime("%H:%M:%S  %d.%m.%y")

        pref = (" " + str(pref) + ": ") if pref != "" else ""
        app_name = ("Приложение: " + str(app_name) + ". ") if app_name != "" else ""
        scenario_start = ("Начало сценария: " + str(scenario_start) + ". ") if scenario_start != "" else ""
        scenario_end = ("Конец сценария: " + str(scenario_end) + ". ") if scenario_end != "" else ""
        condition = ("Условие: " + str(condition) + ". ") if condition != "" else ""
        comment = ("Комментарий: " + str(comment) + ". ") if comment != "" else ""
        variable = ("Значение переменной: " + str(variable) + ". ") if variable != "" else ""
        user_id = ("user_id: " + str(user_id) + ". ") if user_id != "" else ""
        user_name = ("user_name: " + str(user_name) + ". ") if user_name != "" else ""
        message = ("Сообщение: " + str(message) + ". ") if message != "" else ""

        print(text_color + f"{time_now} | "
                           f"{pref}"
                           f"{user_id}"
                           f"{user_name}"
                           f"{app_name}"
                           f"{scenario_end}"
                           f"{scenario_start}"
                           f"{condition}"
                           f"{variable}"
                           f"{comment}"
                           f"{message}")


if __name__ == "__main__":
    x = 10
    debug_log(True, variable=f"{x=}")
