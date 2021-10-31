from os import remove, urandom

import pytest

from tests.unit.conftest import fixture_path, tmp_path
from whispers.core.args import parse_args
from whispers.core.log import configure_log, global_exception_handler


@pytest.mark.parametrize(("create", "expected"), [(False, None), (True, tmp_path("whispers.log"))])
def test_configure_log(create, expected):
    args = []
    if create:
        args = ["--log"]

    args.append(fixture_path())
    result = configure_log(parse_args(args))
    if result:
        assert result.exists()
        result = result.as_posix()
        remove(result)

    assert result == expected


def test_global_exception_handler():
    args = parse_args(["-l", fixture_path()])
    logfile = configure_log(args)
    message = urandom(30).hex()
    try:
        1 / 0

    except Exception:
        global_exception_handler(logfile.as_posix(), message)

    logtext = logfile.read_text()

    assert "ZeroDivisionError: division by zero" in logtext
    assert message in logtext
