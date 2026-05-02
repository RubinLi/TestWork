import logging
import argparse
from abc import ABC, abstractmethod
from pathlib import Path
import sys
from tabulate import tabulate


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
        log_file: str | None = 'testwork.log',

    ):
        self.log_file: Path | None
        self.workdir = Path(__file__).resolve().parent
        self.log_level = log_level
        if log_file:
            self.log_file = self.workdir.joinpath(log_file)
        else:
            self.log_file = None


def argparsess(logic) -> tuple[list, str]:
    """
    Разбирает аргументы командой строки

    Параметры
    ---------
    lodic : list
        Список типов отчетов, содержащих логику расчетов.
        Используется для ограничения ввода пользователя,
        существующими типами отчетов.

    Возвращаемое значение
    ---------------------
    [list,str] : tumple
        Кортеж содержащий список файлов и тип отчёта.
    """
    str_args_files_help: str = "Имена csv-файлов с метриками видео на YouTube (может быть несколько)"
    str_args_report_help: str = "Тип отчёта, отвечает за логикy расчётов"
    str_prog_info: str = "testWork"
    parser = argparse.ArgumentParser(
        prog=str_prog_info)
    parser.add_argument('-f',
                        '--files',
                        type=str,
                        nargs='+',
                        required=True,
                        help=str_args_files_help)
    parser.add_argument('-r', '--report',
                        type=str,
                        help=str_args_report_help,
                        required=True,
                        choices=sorted(logic),
                        nargs=1)
    args: argparse.Namespace = parser.parse_args()

    str_info_argparse: str = f"Извлекаю аргументы CLI"
    str_debug_argparse: str = str_info_argparse + (
        f" -> Список файлов: {args.files}, Логика отчёта: {args.report[0]}")
    logging.info(msg=str_info_argparse)
    logging.debug(msg=str_debug_argparse)
    return args.files, args.report[0]


def checking_files_exists(files):
    """
    Проверяет существование файлов

    Параметры
    ---------
    files : list
        Список путей к файлам, для проверки существования

    Возвращаемое значение
    ---------------------
    Bool
        Возвращает False если хотя бы один из файлов не существует
        Возвращает True  если все файлы существуют
    """
    missing_files = [f for f in files if not Path(f).exists()]
    if missing_files:
        for missing_file in missing_files:
            print(f"Файлы отсутствует по пути {missing_file}")
        return False
    str_info_files_exist: str = f"Проверяю наличие файлов статистики"
    str_debug_files_exist: str = str_info_files_exist + (
        f" -> Файлы существуют: {files}")
    logging.info(msg=str_info_files_exist)
    logging.debug(msg=str_debug_files_exist)
    return True


class Report():
    """
    Класс представляет интерфейс для работы с логикой отчетов.

    Атрибуты
    ---------
    logic : Logic
        Класс представляющий логику генерации отчетов
    data: list
        Обработанные в рамках генерации отчета данные.

    """

    def __init__(self, logic) -> None:
        self._logic = logic
        self._data = []

    def report_data_from_files(self, files: list):
        self._data = self._logic.report_from_files(files)
        return self

    def report_table(self) -> str:
        return self._logic.report_table(self._data)

    def report_text(self) -> None:
        print("функция ещё не реализована")
        pass


class Logic(ABC):

    @abstractmethod
    def report_from_files(self, files) -> list:
        pass

    @abstractmethod
    def report_table(self, data) -> str:
        pass


class Clickbait(Logic):
    """
    Класс работающий с информацией о видео  привлекающих внимание

    ...

    Атрибуты
    --------
    fieldtype : dict
        словарь хранящий список полей для оценки
        привлекательности видео, и соответствующие функции
        для приведения значений полей к типу, подходящему для oценки.
        Пример:

        fieldtype = {'title': int, 'ctr': float, 'retention_rate': float}

    above_ctr: float
            нижнее значение кликабельности
    below_retention_rate: float
            Верхнее значение удержания
    """

    def __init__(self, above_ctr=15.0, below_retention_rate=40.0) -> None:
        self.fieldtype: dict = {
            'title': str,
            'ctr': float,
            'retention_rate': float}

        self.above_ctr: float = above_ctr
        self.below_retention_rate: float = below_retention_rate

    def _extract_from_files(self, files: list) -> list:
        """
        Извлекает данные для анализа привлекательности видео
        из csv файлов и возвращает список объединённых  данных
        из нескольких файлов

        Параметры
        ---------
        additional : list
            список путей к csv файлам, для извлечения данных

        Возвращаемое значение
        ---------------------
        union_list_of_video : list
            список объединённых данных для анализа привлекательности
        """
        # TODO: если часть файлов не обработана продолжить работу опционально
        union_list_of_video: list = []
        for file in files:
            list_of_video: list | None = self._read_csv_file(
                file_csv_patch=file,
                fieldtype=self.fieldtype)
            if list_of_video:
                union_list_of_video: list = union_list_of_video + list_of_video

        str_info_filter: str = f"Записи извлечены из файлов: {files}"
        str_debug_filter: str = str_info_filter + f" -> {union_list_of_video}"
        logging.info(msg=str_info_filter)
        logging.debug(msg=str_debug_filter)
        return union_list_of_video

    def _filter(self, data) -> list:
        """
        Выбирает информацию о видео
        ,удовлетворяющих критериям привлекательности,
        и возвращает в виде списка

        Параметры
        ---------
        additional : list
            список путей к csv файлам, для извлечения данных

        Возвращаемое значение
        ---------------------
        fields : List
            Список отфильтрованных данных
        """
        filtered = [line for line in data
                    if line["ctr"] > self.above_ctr and
                    line["retention_rate"] < self.below_retention_rate
                    ]

        str_info_filter: str = (f"Фильтрую записи огласно условию: "
                                f" ctr > {self.above_ctr} retrntion_rate < {self.below_retention_rate}")
        str_debug_filter: str = str_info_filter + f" -> {filtered}"
        logging.info(msg=str_info_filter)
        logging.debug(msg=str_debug_filter)
        return filtered

    def _sorted_data_decres_csv(self, data: list) -> list:
        """
        Cортирует информацию о видео по убыванию csv:

        Параметры
        ---------
        data: list
            список строк для сортировки

        sorted_by_csv_desc : List
            Сортированный список
        """
        sorted_by_csv_desc = sorted(
            data, key=lambda d: d.get("ctr"), reverse=True)

        str_info_sorted: str = "Сортирую записи по убыванию ctr: "
        str_debug_sorted: str = str_info_sorted + f" -> {sorted_by_csv_desc}"
        logging.info(msg=str_info_sorted)
        logging.debug(msg=str_debug_sorted)
        return sorted_by_csv_desc

    def report_from_files(self, files: list):
        """
        Подготавливает данные из файлов для генерации отчета

        Параметры
        ---------
        data: files
            список путей к файлам.

        final_date : List
            подготовленные данные
        """
        files = self._extract_from_files(files)
        filter_date = self._filter(files)
        final_date = self._sorted_data_decres_csv(filter_date)
        str_info_report: str = "Заканчиваю подготовку данных: "
        str_debug_report: str = str_info_report + f" -> {filter_date}"
        logging.info(msg=str_info_report)
        logging.debug(msg=str_debug_report)
        return final_date

    def report_table(self, data) -> str:
        """
        Подготавливает данные из файлов для генерации отчета

        Параметры
        ---------
        data: files
            список путей к файлам.

        final_date : List
            подготовленные данные
        """
        table = tabulate(data,
                         headers='keys',
                         tablefmt="grid",
                         colalign=("left", "center", "right"),
                         missingval="N/A")
        str_info_table: str = "Подготавливаю отчет в виде таблицы: "
        str_debug_table: str = str_info_table + f" -> {table}"
        logging.info(msg=str_info_table)
        logging.debug(msg=str_debug_table)
        return table

    def _read_csv_file(self, file_csv_patch, fieldtype) -> list[dict] | None:
        """
        Читает из csv файла набор полей указанных в параметре fieldtype
        и преобразует к необходимым типам.

        Параметры
        ---------
        file_patch : str

            Путь к файлу

        fieldtype : dict

            Словарь содержит набор полей для считывания из csv файла.
            и соответствующие функции для преобразования типов.

        Возвращаемое значение
        ---------------------
        list | none
            Возвращает список словарей, 
            каждый словарь
            представляет собой строку csv файла.

            В случаею ошибки чтения none.

        """
        # TODO: Реализовать более строгую обвязку для
        # преобразования CSV файла в словарь.
        class CSVFieldNotFoundError(Exception):
            """Запрошеное поле отсутствует в csv файле"""
        import csv
        list = []
        missing = {}

        def filter_and_type_set(line, fieldtype):
            return {
                k: (v if k is str else fieldtype[k](v))
                for k, v in line.items()
                if k in fieldtype
            }
        try:
            with open(file=file_csv_patch) as f:
                dictreader = csv.DictReader(f)
                # next(dictreader)
                for line in dictreader:
                    # checking_field(line, fieldtype)
                    missing = set(fieldtype) - set(line)
                    if missing:
                        raise (CSVFieldNotFoundError)
                    list.append(filter_and_type_set(line,  fieldtype))
            str_debug_read_csv: str = (
                f"Данные из файла csv ({file_csv_patch}): {list}")
            str_info_read_csv: str = f"Читаю csv файл {file_csv_patch}"
            logging.info(msg=str_info_read_csv)
            logging.debug(msg=str_debug_read_csv)
            return list
        except FileNotFoundError:
            str_warning_not_found: str = f"csv файл не найден! по пути{
                file_csv_patch}"
            logging.warning(msg=str_warning_not_found)
            return None
        except CSVFieldNotFoundError:
            str_warning_not_found: str = f"csv поле {
                missing} не найдено в файле {file_csv_patch}"
            logging.warning(msg=str_warning_not_found)
            return None
        except ValueError as errortext:
            str_warning_valueerror: str = (
                f"Ошибка преобразования поля в новый тип: {
                    errortext}")
            logging.warning(msg=str_warning_valueerror)
            return None


def main():
    input_files: list
    selected_logic: str
    settings = Settings(log_level=logging.INFO, log_file='newlogfile.log')
    logging.basicConfig(level=settings.log_level, filename=settings.log_file,
                        format="%(asctime)s %(funcName)s %(levelname)s: %(message)s")
    logic_dict: dict = {
        "Clickbait": Clickbait(above_ctr=12, below_retention_rate=40),
        "Clickbait1": Clickbait(above_ctr=24, below_retention_rate=30)
    }
    logging.info(msg="Запуск")

    input_files, selected_logic = argparsess(logic=logic_dict.keys())
    # print(input_files)
    if not checking_files_exists(files=input_files):
        print("Утилита завершает работу!")
        sys.exit(1)

    report_table: str = (Report(logic=logic_dict[selected_logic])
                         .report_data_from_files(files=input_files)
                         .report_table())

    print("Таблица: Кликбейтные видео:")
    print(report_table)


if __name__ == "__main__":
    main()
