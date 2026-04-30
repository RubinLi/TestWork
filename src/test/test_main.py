from src.testWork.main import *  # content of test_sample.py
from unittest.mock import patch

import sys
from pathlib import Path

import pytest


class TestArgparse:
    def test_argparsess_only_arg_files(self, capsys):
        with patch("sys.argv", ["main", "--files", "sss", "1"]):
            files, report = argparsess()
            assert files == ["sss", "1"] and report == None

    def test_argparsess_only_arg_report(self, capsys):
        with patch("sys.argv", ["main", "--report", "report_type"]):
            files, report = argparsess()
            assert files == None and report == "report_type"

    def test_error_argparses_many_values_report(self, capsys):
        with pytest.raises(SystemExit) as excinfo:
            with patch("sys.argv", ["main", "--repor", "report_type", "error"]):
                argparsess()
        assert excinfo.value.code != 0
        terminal = capsys.readouterr()
        assert "error: unrecognized arguments" in terminal.err


class TestCSVread:
    # TODO: Проверка обработки исключений через логер, или проброс ошибок в стиле
    # wrap.
    DATA_DIR = Path(__file__).resolve().parent.parent / "files"
    FIELD_TYPE = {'title': str, 'ctr': float, 'retention_rate': float}
    FIELD_NO_FOUND = {'error_field': str,
                      'ctr': float, 'retention_rate': float}
    FIELD_TYPE_ERROR = {'title': int,
                        'ctr': float, 'retention_rate': float}

    def test_read_csc_file(self):
        likes = '0'
        list_of_video: list | None = read_csv_file(
            file_patch=self.DATA_DIR / 'stats1.csv', fieldtype=self.FIELD_TYPE)
        print(list_of_video)
        if list_of_video:
            for video_info in list_of_video:
                if video_info['title'] == 'Секрет который скрывают тимлиды':
                    likes: str = video_info['ctr']
            assert likes == 25.0
        else:
            assert None == 25.0

    def test_error_csv_files_nofound(self, capsys):
        None_file = read_csv_file(
            file_patch=self.DATA_DIR/'NotFound.csv', fieldtype=self.FIELD_TYPE)
        assert None_file == None

    def test_error_csv_field_nofound(self, capfd):
        None_file = read_csv_file(
            file_patch=self.DATA_DIR/'stats1.csv', fieldtype=self.FIELD_NO_FOUND)
        assert None_file == None

    def test_error_csv_field_type_conver(self, capfd):
        None_file = read_csv_file(
            file_patch=self.DATA_DIR/'stats1.csv', fieldtype=self.FIELD_TYPE_ERROR)
        assert None_file == None
