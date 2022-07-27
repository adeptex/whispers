import pytest

from tests.unit.conftest import fixture_path
from whispers.core.args import parse_args
from whispers.main import main, run


def test_main():
    with pytest.raises(SystemExit):
        main()


def test_run():
    args = parse_args([fixture_path()])
    secrets = list(run(args))
    assert len(secrets) == 307


# def test_global_exception_handler():
#     args = parse_args(["-l", fixture_path()])
#     message = urandom(30).hex()
#     try:
#         1 / 0

#     except Exception:
#         global_exception_handler(logfile.as_posix(), message)

#     logtext = logfile.read_text()

#     assert "ZeroDivisionError: division by zero" in logtext
#     assert message in logtext
