import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import gettempdir

import pytest

from whispers.models.rule import Rule

FIXTURE_PATH = Path("tests/fixtures")
CONFIG_PATH = Path("tests/configs")
RULE_PATH = Path("tests/rules")


@contextmanager
def does_not_raise():
    yield


@pytest.fixture
def rule_fixture():
    return Rule({"id": "fixture", "message": "test", "severity": "INFO", "key": {}, "value": {}})


def fixture_path(filename: str = "") -> str:
    return FIXTURE_PATH.joinpath(filename).as_posix()


def config_path(filename: str = "") -> str:
    return CONFIG_PATH.joinpath(filename).as_posix()


def rule_path(filename: str = "") -> str:
    return RULE_PATH.joinpath(filename).as_posix()


def forbidden_path() -> str:
    # Linux & MacOS
    if os.name == "posix":
        return "/root/403"

    # Windows
    return Path("%windir%\\system32\\config\\SAM").resolve().as_posix()


def tmp_path(filename: str = "") -> str:
    return Path(gettempdir()).resolve().joinpath(filename).as_posix()
