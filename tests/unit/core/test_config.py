import re
from os import devnull, urandom

import pytest

from tests.unit.conftest import config_path, does_not_raise, tmp_path
from whispers.core.args import parse_args
from whispers.core.config import load_config


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        (tmp_path(f"file-404-{urandom(30).hex()}"), pytest.raises(FileNotFoundError)),
        (devnull, pytest.raises(TypeError)),
        (config_path("invalid.yml"), pytest.raises(RuntimeError)),
        (config_path("empty.yml"), pytest.raises(RuntimeError)),
        (config_path("example.yml"), does_not_raise()),
    ],
)
def test_load_config_exception(filename, expected):
    with expected:
        args = parse_args(["-c", filename, "src"])
        load_config(args)


def test_load_config():
    args = parse_args(["-c", config_path("example.yml"), "src"])
    config = load_config(args)
    assert config.exclude.files == re.compile(r"\.npmrc|.*coded.*|\.git/.*")
    assert config.exclude.keys == re.compile("SECRET_VALUE_KEY")
    assert config.exclude.values == re.compile("SECRET_VALUE_PLACEHOLDER")
