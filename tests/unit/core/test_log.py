from os import remove, urandom

import pytest

from tests.unit.conftest import fixture_path
from whispers.core.args import parse_args
from whispers.core.log import cleanup_log, configure_log, global_exception_handler


def test_configure_log():
    args = parse_args([fixture_path()])
    expected_file = configure_log(args)
    assert expected_file.exists()

    try:
        remove(expected_file.as_posix())

    except PermissionError:
        pass


@pytest.mark.parametrize(
    ("data", "expected"), [("", False), ("a", True),],
)
def test_cleanup_log(data, expected):
    args = parse_args([fixture_path()])
    logfile = configure_log(args)
    logfile.write_text(data)
    cleanup_log()
    assert logfile.exists() == expected

    if logfile.exists():
        try:
            remove(logfile)

        except (PermissionError, OSError):
            pass


def test_global_exception_handler():
    args = parse_args([fixture_path()])
    logfile = configure_log(args)
    message = urandom(30).hex()
    try:
        1 / 0

    except Exception:
        global_exception_handler(logfile.as_posix(), message)

    logtext = logfile.read_text()

    assert "ZeroDivisionError: division by zero" in logtext
    assert message in logtext
