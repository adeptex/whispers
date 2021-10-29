import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import gettempdir

FIXTURE_PATH = Path("tests/fixtures")
CONFIG_PATH = Path("tests/configs")
RULE_PATH = Path("tests/rules")


@contextmanager
def does_not_raise():
    yield


def fixture_path(filename: str = "") -> str:
    return FIXTURE_PATH.joinpath(filename).as_posix()


def config_path(filename: str = "") -> str:
    return CONFIG_PATH.joinpath(filename).as_posix()


def rule_path(filename: str = "") -> str:
    return RULE_PATH.joinpath(filename).as_posix()


def forbidden_path() -> str:
    if os.name == "posix":
        return "/root/403"  # Linux & MacOS

    return Path("%windir%\\system32\\config\\SAM").resolve().as_posix()  # Windows


def tmp_path(filename: str = "") -> str:
    return Path(gettempdir()).resolve().joinpath(filename).as_posix()
