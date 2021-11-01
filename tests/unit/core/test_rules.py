import pytest

from tests.unit.conftest import config_path, does_not_raise
from whispers.core.args import parse_args
from whispers.core.config import load_config
from whispers.core.rules import _ensure_exists, default_rule_structure, load_rules
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
    args = parse_args(["-r", "npmrc,pypirc,pip", "tests/fixtures"])
    config = load_config(args)
    rules = load_rules(args, config)
    assert len(rules) == 3


def test_load_rules_severity():
    args = parse_args(["-s", "BLOCKER,CRITICAL", "tests/fixtures"])
    config = load_config(args)
    rules = load_rules(args, config)
    assert len(rules) == 11


@pytest.mark.parametrize(
    ("rule", "expected"),
    [
        ({}, pytest.raises(IndexError)),
        ({"id": "i"}, pytest.raises(IndexError)),
        ({"id": "i", "key": "k"}, pytest.raises(IndexError)),
        ({"id": "i", "key": "k", "value": "v"}, pytest.raises(IndexError)),
        ({"id": "i", "key": "k", "value": "v", "message": "m"}, pytest.raises(IndexError)),
        ({"id": "i", "key": "k", "value": "v", "message": "m", "severity": "s"}, does_not_raise()),
    ],
)
def test_default_rule_structure(rule, expected):
    with expected:
        default_rule_structure(rule)


@pytest.mark.parametrize(
    ("key", "rule", "expected"), [("id", {}, pytest.raises(IndexError)), ("id", {"id": "i"}, does_not_raise()),],
)
def test_ensure_exists(key, rule, expected):
    with expected:
        _ensure_exists(key, rule)
