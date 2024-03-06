import re

import pytest
from yaml import safe_load

from tests.unit.conftest import RULE_PATH, does_not_raise
from whispers.models.pair import KeyValuePair
from whispers.models.rule import Rule, Specification


def test_rule():
    yml = safe_load(RULE_PATH.joinpath("valid.yml").read_text())[0]
    rule = Rule(yml)
    assert rule.id == "valid"
    assert rule.message == "Valid"
    assert rule.severity == "Info"
    assert rule.key is None
    assert rule.value.regex == re.compile(r"^test$")
    assert rule.value.ignorecase is False


@pytest.mark.parametrize(
    ("rule", "expected"),
    [
        ({}, pytest.raises(IndexError)),
        ({"id": "i", "group": "g"}, pytest.raises(IndexError)),
        ({"id": "i", "group": "g", "key": "k"}, pytest.raises(IndexError)),
        ({"id": "i", "group": "g", "key": "k", "value": "v"}, pytest.raises(IndexError)),
        ({"id": "i", "group": "g", "key": "k", "value": "v", "message": "m"}, pytest.raises(IndexError)),
        (
            {"id": "i", "group": "g", "key": "k", "value": "v", "message": "m", "severity": "s"},
            pytest.raises(ValueError),
        ),
        ({"id": "i", "group": "g"}, pytest.raises(IndexError)),
        ({"id": "i"}, pytest.raises(IndexError)),
        ({"id": "i", "group": "g", "message": "m"}, pytest.raises(IndexError)),
        ({"severity": "s", "message": "m"}, pytest.raises(IndexError)),
        ({"id": "i", "group": "g", "severity": "s"}, pytest.raises(IndexError)),
        ({"id": "i", "group": "g", "message": "m", "severity": "s"}, does_not_raise()),
        ({"id": "i", "group": "g", "key": {}, "message": "m", "severity": "s"}, does_not_raise()),
        ({"id": "i", "group": "g", "value": {}, "message": "m", "severity": "s"}, does_not_raise()),
        ({"id": "i", "group": "g", "key": {}, "value": {}, "message": "m", "severity": "s"}, does_not_raise()),
        ({"id": "i", "group": "g", "message": "m", "severity": "s", "key": {"minlen": 1}}, does_not_raise()),
        ({"id": "i", "group": "g", "message": "m", "severity": "s", "value": {"regex": "a"}}, does_not_raise()),
        ({"id": "i", "group": "g", "message": "m", "severity": "s", "similar": 0.5}, does_not_raise()),
    ],
)
def test_rule_structure(rule, expected):
    with expected:
        key = rule.get("key", None)
        value = rule.get("value", None)
        result = Rule(rule)

        assert result.id == rule.get("id", None)
        assert result.message == rule.get("message", None)
        assert result.severity == rule.get("severity", None)
        assert result.similar == rule.get("similar", 1)

        if key:
            assert result.key == Specification(**key)

        else:
            assert result.key is None

        if value:
            assert result.value == Specification(**value)

        else:
            assert result.value is None


@pytest.mark.parametrize(
    ("idx", "expected"),
    [
        ("id", does_not_raise()),
        ("missing", pytest.raises(IndexError)),
    ],
)
def test_rule_get_required(idx, expected, rule_fixture):
    rule = {"id": "test"}
    with expected:
        rule_fixture._get_required(idx, rule)


@pytest.mark.parametrize(
    ("idx", "expected"),
    [
        ("key", Specification(minlen=1)),
        ("value", None),
    ],
)
def test_rule_get_spec(idx, expected, rule_fixture):
    rule_fixture.key = {"minlen": 1}
    rule_fixture.value = {}

    assert rule_fixture._get_spec(idx, rule_fixture.__dict__) == expected


@pytest.mark.parametrize(
    ("idx", "expected"),
    [
        ("key", True),
        ("value", False),
    ],
)
def test_rule_matches_spec(idx, expected, rule_fixture):
    pair = KeyValuePair("sonar.jdbc.password", "a")
    rule_fixture.__dict__[idx] = Specification(**{"regex": r"sonar\.jdbc\.password"})

    assert rule_fixture.matches(pair) is expected


@pytest.mark.parametrize(
    ("idx", "regex", "ignorecase", "expected"),
    [
        ("key", r"ke.*", True, True),
        ("key", r"Ke.*", False, False),
        ("key", r"a.*", True, False),
        ("value", r"tes.*", True, True),
        ("value", r"Tes.*", False, False),
        ("value", r"a.*", True, False),
    ],
)
def test_rule_matches_regex(idx, regex, ignorecase, expected, rule_fixture):
    pair = KeyValuePair("key", "test")
    rule_fixture.__dict__[idx] = Specification(**{"regex": regex, "ignorecase": ignorecase})

    assert rule_fixture.matches(pair) is expected


@pytest.mark.parametrize(
    ("value", "isBase64", "isAscii", "isUri", "isLuhn", "expected"),
    [
        ("test", True, True, True, True, False),
        ("test", True, True, True, False, False),
        ("test", True, True, False, True, False),
        ("dGVzdAo=", True, True, False, False, True),
        ("test", True, False, True, True, False),
        ("test", True, False, True, False, False),
        ("test", True, False, False, True, False),
        (b"test", True, False, False, False, True),
        ("test", False, True, True, True, False),
        ("http://localhost.localdomain", False, True, True, False, True),
        ("4111111111111111", False, True, False, True, True),
        ("test", False, True, False, False, True),
        ("test", False, False, True, True, False),
        ("http://localhost.localdomain", False, False, True, False, False),
        (b"4111111111111111", False, False, False, True, False),
        (b"test", False, False, False, False, False),
    ],
)
def test_rule_matches_param(value, isBase64, isAscii, isUri, isLuhn, expected, rule_fixture):
    pair = KeyValuePair("key", value)
    rule_fixture.value = Specification(
        **{
            "isBase64": isBase64,
            "isAscii": isAscii,
            "isUri": isUri,
            "isLuhn": isLuhn,
        }
    )

    assert rule_fixture.matches(pair) is expected


@pytest.mark.parametrize(
    ("minlen", "expected"),
    [
        (0, True),
        (4, True),
        (5, False),
    ],
)
def test_rule_matches_minlen(minlen, expected, rule_fixture):
    pair = KeyValuePair("key", "test")
    rule_fixture.value = Specification(**{"minlen": minlen})

    assert rule_fixture.matches(pair) is expected


@pytest.mark.parametrize(
    ("key", "value", "similar", "expected"),
    [
        ("key", "KEY", 1, False),
        ("key", "KEY", 0, False),
        ("key", "value", 0.3, True),
        ("key", "value", 0, False),
    ],
)
def test_rule_matches_similar(key, value, similar, expected, rule_fixture):
    pair = KeyValuePair(key, value)
    rule_fixture.similar = similar

    assert rule_fixture.matches(pair) is expected


@pytest.mark.parametrize(
    ("isFile", "expected"),
    [
        (False, False),
        (True, True),
    ],
)
def test_rule_matches_isfile(isFile, expected, rule_fixture):
    pair = KeyValuePair("file", "tests/fixtures/test.txt")
    rule_fixture.value = Specification(regex=re.compile(".*test.*"), isFile=isFile)

    assert rule_fixture.matches(pair) is expected
