from argparse import ArgumentParser
from io import StringIO, TextIOWrapper
from logging import FileHandler, StreamHandler
from os import remove, urandom
from re import compile
from sys import stdout
from unittest.mock import patch

import pytest

from tests.unit.conftest import config_path, does_not_raise, tmp_path
from whispers.__version__ import __version__, __whispers__
from whispers.core.args import argument_parser, parse_args, show_config, show_info, show_splash


def test_argument_parser():
    assert isinstance(argument_parser(), ArgumentParser)


@pytest.mark.parametrize(
    ("arguments", "key", "expected", "exception"),
    [
        (["src"], "src", "src", does_not_raise()),
        (["src"], "output", stdout, does_not_raise()),
        (
            ["-c", config_path("detection_by_value.yml"), "src"],
            "config",
            config_path("detection_by_value.yml"),
            does_not_raise(),
        ),
        (["-r", "rule-1,rule-2", "src"], "rules", ["rule-1", "rule-2"], does_not_raise()),
        (["-e", "123", "src"], "exitcode", 123, does_not_raise()),
        (["-s", "a,b,c", "src"], "severity", ["a", "b", "c"], does_not_raise()),
        (["-f", "*.json", "src"], "files", ["*.json"], does_not_raise()),
        (["-F", ".*\\.(yml|json)", "src"], "xfiles", compile(r".*\.(yml|json)"), does_not_raise()),
        (["--info"], "info", True, pytest.raises(SystemExit)),
        (["--debug"], "debug", True, pytest.raises(SystemExit)),
        (["--init"], "init", True, pytest.raises(SystemExit)),
    ],
)
def test_parse_args(arguments, key, expected, exception):
    with exception:
        args = parse_args(arguments)
        assert args.__dict__[key] == expected


@pytest.mark.parametrize(
    ("arguments", "key", "expected", "exception"),
    [
        (["--log", "log.txt", "src"], "log", FileHandler, does_not_raise()),
        (["src"], "log", StreamHandler, does_not_raise()),
    ],
)
def test_parse_args_log(arguments, key, expected, exception):
    with exception:
        args = parse_args(arguments)
        assert isinstance(args.__dict__[key], expected)

    try:
        remove("log.txt")
    except BaseException:
        pass


def test_parse_args_output():
    outfile = tmp_path(f"out-{urandom(30).hex()}")
    args = parse_args(["--output", outfile, "src"])
    assert isinstance(args.output, TextIOWrapper)
    args.output.close()
    remove(outfile)


def test_show_info():
    mock_print = StringIO()
    with patch("sys.stdout", mock_print):
        show_info()
        result = mock_print.getvalue()
        expected = ["keys", "apikey-known", "High"]
        for item in expected:
            assert item in result


def test_show_splash():
    mock_print = StringIO()
    with patch("sys.stdout", mock_print):
        show_splash(lambda: 1)()
        result = mock_print.getvalue()
        expected = [__version__, __whispers__]
        for item in expected:
            assert item in result


def test_show_config():
    mock_print = StringIO()
    with patch("sys.stdout", mock_print):
        show_config()
        result = mock_print.getvalue()
        expected = ["include", "exclude"]
        for item in expected:
            assert item in result
