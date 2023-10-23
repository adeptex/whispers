import pytest

from tests.unit.conftest import config_path
from whispers.core.args import parse_args
from whispers.core.config import load_config
from whispers.core.rules import load_rules
from whispers.core.utils import default_rules


@pytest.mark.parametrize(
    ("configfile", "expected"),
    [("example.yml", len(default_rules())), ("example_rules.yml", 2), ("inline_rule.yml", 3)],
)
def test_load_rules(configfile, expected):
    args = parse_args(["-c", config_path(configfile), "tests/fixtures"])
    config = load_config(args)
    rules = load_rules(args, config)
    assert len(rules) == expected


def test_load_rules_ids():
    args = parse_args(["-r", "npmrc,pypirc,pip,apikey", "-R", "apikey", "tests/fixtures"])
    config = load_config(args)
    rules = load_rules(args, config)
    assert len(rules) == 3


def test_load_rules_groups():
    args = parse_args(["-g", "python,files", "-G", "files", "tests/fixtures"])
    config = load_config(args)
    rules = load_rules(args, config)
    assert len(rules) == 2


def test_load_rules_severity():
    args = parse_args(["-s", "Critical,High,Low", "-S", "Low", "tests/fixtures"])
    config = load_config(args)
    rules = load_rules(args, config)
    assert len(rules) == 11
