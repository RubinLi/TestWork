# import pyglet
from src.testWork.main import *  # content of test_sample.py
from unittest.mock import patch

import sys
from pathlib import Path

import pytest

# TODO: Сформировать тестовые данные и вынести в фикстуры.


class TestArgparse:
    @pytest.mark.skipif(reason="новая логика")
    def test_argparsess_only_arg_files(self, capsys):
        with patch("sys.argv", ["main", "--files", "sss", "1"]):
            files, report = argparsess()
            assert files == ["sss", "1"] and report == None

    @pytest.mark.skipif(reason="новая логика")
    def test_argparsess_only_arg_report(self, capsys):
        with patch("sys.argv", ["main", "--report", "report_type"]):
            files, report = argparsess()
            assert files == None and report == "report_type"

    def test_argparses_values_report(self, capsys):
        with patch("sys.argv", ["main",
                                "--files", "f1",
                                "--report", "Clickbate"]):
            files, report = argparsess(["Clickbate"])
            assert files == ["f1"] and report == "Clickbate"

    def test_error_argparses_values_report(self, capsys):

        with pytest.raises(SystemExit) as excinfo:
            with patch("sys.argv", ["main",
                                    "--files", "f1",
                                    "--report", "error"]):
                argparsess(["Clickbate"])
        assert excinfo.value.code != 0
        terminal = capsys.readouterr()
        assert "(choose from " in terminal.err


class Testfiles_exists():
    DATA_DIR = Path(__file__).resolve().parent

    def test_file_exist(self):
        exist = checking_files_exists(
            [self.DATA_DIR.joinpath("files", "stats1.csv"),
             self.DATA_DIR.joinpath("files", "stats2.csv")])
        assert True == exist

    def test_error_no_file_exist(self):
        exist = checking_files_exists(
            [self.DATA_DIR.joinpath("files", "error.csv")])
        assert False == exist


class TestCSVread:
    # TODO: Проверка обработки исключений через логер, или проброс ошибок в стиле
    # wrap.
    DATA_DIR = Path(__file__).resolve().parent.parent.joinpath("files")
    FIELD_TYPE = {'title': str, 'ctr': float, 'retention_rate': float}
    FIELD_NO_FOUND = {'error_field': str,
                      'ctr': float, 'retention_rate': float}
    FIELD_TYPE_ERROR = {'title': int,
                        'ctr': float, 'retention_rate': float}
    clickbate = Clickbait(above_ctr=12, below_retention_rate=40)

    def test_read_csc_file(self):
        likes = '0'
        list_of_video: list | None = self.clickbate._read_csv_file(
            file_csv_patch=self.DATA_DIR.joinpath('stats1.csv'), fieldtype=self.FIELD_TYPE)
        print(list_of_video)
        if list_of_video:
            for video_info in list_of_video:
                if video_info['title'] == 'Секрет который скрывают тимлиды':
                    likes: str = video_info['ctr']
        assert likes == 25.0

    def test_error_csv_files_nofound(self, capsys):
        None_file = self.clickbate._read_csv_file(
            file_csv_patch=self.DATA_DIR.joinpath('NotFound.csv'), fieldtype=self.FIELD_TYPE)
        assert None_file is None

    def test_error_csv_field_nofound(self, capfd):
        None_file = self.clickbate._read_csv_file(
            file_csv_patch=self.DATA_DIR.joinpath('stats1.csv'), fieldtype=self.FIELD_NO_FOUND)
        assert None_file is None

    def test_error_csv_field_type_conver(self, capfd):
        None_file = self.clickbate._read_csv_file(
            file_csv_patch=self.DATA_DIR.joinpath('stats1.csv'), fieldtype=self.FIELD_TYPE_ERROR)
        assert None_file is None


class TestClicbatefiltersuccess():
    data = [{'title': 'success', 'ctr': 13, 'retention_rate': 30},
            {'title': 'fail crt', 'ctr': 9.5, 'retention_rate': 30.0},
            {'title': 'fail rait', 'ctr': 13, 'retention_rate': 82.0}]
    DATA_DIR = Path(__file__).resolve().parent.parent / "files"
    clickbate = Clickbait(above_ctr=12, below_retention_rate=40)

    def test_filter(self):
        filtered = self.clickbate._filter(self.data)
        assert 1 == len(filtered)
        assert filtered[0]["title"] == "success"

    def test_sorted(self):
        sorted = self.clickbate._sorted_data_decres_csv(self.data)
        assert sorted[0]['ctr'] == 13

    def test_extract_from_files(self):
        result = self.clickbate._extract_from_files(
            [self.DATA_DIR.joinpath('stats1.csv'),
             self.DATA_DIR.joinpath('stats2.csv')]
        )
        find0 = list(filter(lambda d: "в 5 утра" in d.get("title"), result))
        find1 = list(filter(lambda d: "4" in d.get("title"), result))

        assert find0[0]['ctr'] == 17.0
        assert find1[0]['ctr'] == 22.5
