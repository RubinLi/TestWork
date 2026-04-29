import logging
import os


class Settings:
    """
    Класс для хранения настроек утилиты.

    ...

    Атрибуты
    --------
    log_file : str
        Путь к файлу журналирования
    log_level : int
        Уровень журналирования 
    """

    def __init__(
        self,
        log_level=logging.INFO,
        log_file="logfile.log",

    ):
        self.workdir = os.path.dirname(os.path.abspath(__file__))
        self.log_level = log_level
        self.log_file = self.workdir + "/" + log_file


def main():
    setting = Settings(log_level=logging.INFO, log_file="testwork.log")
    logging.basicConfig(level=setting.log_level, filename=setting.log_file,
                        format="%(asctime)s %(levelname)s: %(message)s")
    logging.debug("A DEBUG Message")
    logging.info("An INFO")
    logging.warning("A WARNING")
    logging.error("An ERROR")
    logging.critical("A message of CRITICAL severity")
    inc(3)
    print("Hello from workmate-testwork!")


def inc(x):
    if x > 6:
        return x + 1
    else:
        return x


if __name__ == "__main__":
    main()
