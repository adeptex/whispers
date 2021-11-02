import re

import pytest

from whispers.core.utils import DEFAULT_SEVERITY, default_rules, list_rule_ids
from whispers.models.appconfig import AppConfig


def test_appconfig():
    config = AppConfig({})
    assert config.include.files == ["**/*"]
    assert config.include.rules == list_rule_ids(default_rules())
    assert config.include.severity == DEFAULT_SEVERITY
    assert config.exclude.files is None
    assert config.exclude.keys is None
    assert config.exclude.values is None
    assert config.exclude.rules == []
    assert config.exclude.severity == []


@pytest.mark.parametrize(
    ("config", "expected"),
    [
        ({"include": {"severity": ["BLOCKER"]}, "exclude": {}}, ["BLOCKER"]),
        ({"include": {}, "exclude": {}}, DEFAULT_SEVERITY),
    ],
)
def test_appconfig_severity(config, expected):
    config = AppConfig(config)
    assert config.include.severity == expected
    assert config.exclude.severity == []


@pytest.mark.parametrize(
    ("config", "expected"),
    [({"include": {}, "exclude": {"rules": ["rule-id"]}}, ["rule-id"]), ({"include": {}, "exclude": {}}, []),],
)
def test_appconfig_rules(config, expected):
    config = AppConfig(config)
    assert config.include.rules == list_rule_ids(default_rules())
    assert config.exclude.rules == expected


def test_appconfig_compile():
    config = AppConfig({"exclude": {"files": ["test"]}})
    assert config.exclude.files == re.compile(r"test")
    assert config.exclude.keys is None
    assert config.exclude.values is None
