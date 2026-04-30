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
        log_file: str | None = "logfile.log",

    ):
        self.log_file: str | None
        self.workdir = os.path.dirname(os.path.abspath(__file__))
        self.log_level = log_level
        if log_file:
            self.log_file = self.workdir + "/" + log_file
        else:
            self.log_file = None


def argparsess() -> tuple[dict | None, str | None]:
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


def read_csv_file(file_patch, fieldtype) -> list[dict] | None:
    # TODO: Реализовать более полную обвязку для преобразования CSV файла в словарь.
    class CSVFieldNotFoundError(Exception):
        """Запрошеное поле отсутствует в csv файле"""

    import csv
    list = []
    missing = {}

    def filter_and_type_set(line, fieldtype):
        return {
            k: (v if k == str else fieldtype[k](v))
            for k, v in line.items()
            if k in fieldtype
        }

    try:
        with open(file=file_patch) as f:
            dictreader = csv.DictReader(f)
            next(dictreader)
            for line in dictreader:
                # checking_field(line, fieldtype)
                missing = set(fieldtype) - set(line)
                if missing:
                    raise (CSVFieldNotFoundError)
                list.append(filter_and_type_set(line,  fieldtype))
        str_debug_read_csv: str = f"Данные из файла csv ({file_patch}): {list}"
        str_info_read_csv: str = f"Читаю csv файл {file_patch}"
        logging.info(msg=str_info_read_csv)
        logging.debug(msg=str_debug_read_csv)
        return list
    except FileNotFoundError:
        str_warning_not_found: str = f"csv файл не найден! по пути{
            file_patch}"
        logging.warning(msg=str_warning_not_found)
        return None
    except CSVFieldNotFoundError:
        str_warning_not_found: str = f"csv поле {
            missing} не найдено в файле {file_patch}"
        logging.warning(msg=str_warning_not_found)
        return None
    except ValueError as errortext:
        str_warning_valueerror: str = f"Ошибка преобразования поля в новый тип: {
            errortext}"
        logging.warning(msg=str_warning_valueerror)
        return None


def main():
    settings = Settings(log_level=logging.DEBUG,
                        log_file=None)  # "testwork.log")
    logging.basicConfig(level=settings.log_level, filename=settings.log_file,
                        format="%(asctime)s %(levelname)s: %(message)s")
    files: dict | None
    report: str | None
    # files, report = argparsess()
    fieldtype = {'title': int, 'ctr': float, 'retention_rate': float}
    list_of_video = read_csv_file(
        file_patch=settings.workdir + '/../files/stats1.csv',
        fieldtype=fieldtype)
    print(list_of_video)

    logging.debug("A DEBUG Message")
    logging.info("An INFO")
    logging.warning("A WARNING")
    logging.error("An ERROR")
    logging.critical("A message of CRITICAL severity")
    print("Hello from workmate-testwork!")


if __name__ == "__main__":
    main()
