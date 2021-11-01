import pytest

from whispers.core.utils import DEFAULT_SEVERITY, default_rules, list_rule_ids
from whispers.models.appconfig import AppConfig


def test_appconfig():
    config = AppConfig({})
    assert config.include.files == ["**/*"]
    assert config.exclude.files is None
    assert config.exclude.keys is None
    assert config.exclude.values is None
    assert config.rules == list_rule_ids(default_rules())
    assert config.severity == DEFAULT_SEVERITY


@pytest.mark.parametrize(
    ("config", "expected"),
    [
        ({"include": {}, "exclude": {}, "severity": ["BLOCKER"]}, ["BLOCKER"]),
        ({"include": {}, "exclude": {}}, DEFAULT_SEVERITY),
    ],
)
def test_appconfig_severity(config, expected):
    config = AppConfig(config)
    assert config.severity == expected


@pytest.mark.parametrize(
    ("config", "expected"),
    [
        ({"include": {}, "exclude": {}, "rules": ["rule-id"]}, ["rule-id"]),
        ({"include": {}, "exclude": {}}, list_rule_ids(default_rules())),
    ],
)
def test_appconfig_rules(config, expected):
    config = AppConfig(config)
    assert config.rules == expected
