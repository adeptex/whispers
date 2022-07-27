from os import remove, urandom
from pathlib import Path
from tempfile import gettempdir

import pytest

from tests.unit.conftest import fixture_path
from whispers.core.args import parse_args
from whispers.core.log import global_exception_handler


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
