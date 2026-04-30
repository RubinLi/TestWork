from src.testWork.main import *  # content of test_sample.py
from unittest.mock import patch
import pytest


class Testargparse:
    def test_argparsess_only_arg_files(self, capsys):
        with patch("sys.argv", ["main", "--files", "sss", "1"]):
            files, report = argparsess()
            assert files == ["sss", "1"] and report == None

    def test_argparsess_only_arg_report(self, capsys):
        with patch("sys.argv", ["main", "--report", "report_type"]):
            files, report = argparsess()
            assert files == None and report == "report_type"

    def test_argparsess_error_many_values_report(self, capsys):
        with pytest.raises(SystemExit) as excinfo:
            with patch("sys.argv", ["main", "--repor", "report_type", "error"]):
                argparsess()
        assert excinfo.value.code != 0
        terminal = capsys.readouterr()
        assert "error: unrecognized arguments" in terminal.err
        # assert "the following arguments are required: --fdef test_argparsess_error_many_values_report(self):
