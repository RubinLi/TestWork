import logging
import argparse
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
        if log_file:
            self.log_file = self.workdir + "/" + log_file
        else:
            self.log_file = None


def argparsess():
    str_args_files_help: str = "Имена csv-файлов с метриками видео на YouTube (может быть несколько)"
    str_args_report_help: str = "Тип отчёта, отвечает за логикy расчётов"
    str_prog_info: str = "cli приложение для обработки csv-файлов с метриками видео на YouTube"

    parser = argparse.ArgumentParser(
        prog=str_prog_info)
    parser.add_argument('-f',
                        '--files',
                        type=str,
                        nargs='*',
                        help=str_args_files_help)
    parser.add_argument('-r', '--report',
                        type=str,
                        help=str_args_report_help,
                        nargs='?')
    args: argparse.Namespace = parser.parse_args()
    str_debug_msg: str = f"Аргументы cli > files: {
        args.files}, report: {args.report}"
    logging.debug(msg=str_debug_msg)
    return args.files, args.report


def main():
    setting = Settings(log_level=logging.DEBUG,
                       log_file=None)  # "testwork.log")
    logging.basicConfig(level=setting.log_level, filename=setting.log_file,
                        format="%(asctime)s %(levelname)s: %(message)s")
    files, report = argparsess()
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
