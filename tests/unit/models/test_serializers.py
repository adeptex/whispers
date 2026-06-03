import json
import re

import pytest

from whispers.models.rule import Rule, Specification
from whispers.models.serializers import RuleSerializer, SpecificationSerializer


def test_specification_serializer_to_dict_none():
    assert SpecificationSerializer.to_dict(None) is None


def test_specification_serializer_to_dict_empty():
    assert SpecificationSerializer.to_dict(Specification()) == {"ignorecase": False}


def test_specification_serializer_to_dict_regex_default_flags():
    spec = Specification(regex="abc")
    result = SpecificationSerializer.to_dict(spec)
    assert result == {"regex": "abc", "ignorecase": False}


def test_specification_serializer_to_dict_regex_ignorecase():
    spec = Specification(regex="abc", ignorecase=True)
    result = SpecificationSerializer.to_dict(spec)
    assert result == {"regex": "abc", "ignorecase": True}


@pytest.mark.parametrize(
    ("minlen", "expected_has_key"),
    [
        (0, False),
        (1, True),
        (8, True),
    ],
)
def test_specification_serializer_to_dict_minlen(minlen, expected_has_key):
    result = SpecificationSerializer.to_dict(Specification(minlen=minlen))
    assert ("minlen" in result) is expected_has_key
    if expected_has_key:
        assert result["minlen"] == minlen


@pytest.mark.parametrize("flag", ["isBase64", "isAscii", "isUri", "isLuhn"])
@pytest.mark.parametrize("value", [True, False])
def test_specification_serializer_to_dict_bool_flags_set(flag, value):
    result = SpecificationSerializer.to_dict(Specification(**{flag: value}))
    assert result[flag] is value


@pytest.mark.parametrize("flag", ["isBase64", "isAscii", "isUri", "isLuhn"])
def test_specification_serializer_to_dict_bool_flags_none_omitted(flag):
    result = SpecificationSerializer.to_dict(Specification())
    assert flag not in result


@pytest.mark.parametrize(
    ("isFile", "expected_has_key"),
    [
        (False, False),
        (True, True),
    ],
)
def test_specification_serializer_to_dict_isfile(isFile, expected_has_key):
    result = SpecificationSerializer.to_dict(Specification(isFile=isFile))
    assert ("isFile" in result) is expected_has_key
    if expected_has_key:
        assert result["isFile"] is True


def test_specification_serializer_to_dict_all_fields():
    spec = Specification(
        regex="token|secret",
        ignorecase=True,
        minlen=4,
        isBase64=False,
        isAscii=True,
        isUri=False,
        isLuhn=False,
        isFile=True,
    )
    assert SpecificationSerializer.to_dict(spec) == {
        "regex": "token|secret",
        "ignorecase": True,
        "minlen": 4,
        "isBase64": False,
        "isAscii": True,
        "isUri": False,
        "isLuhn": False,
        "isFile": True,
    }


def test_specification_serializer_regex_flags_reflect_compiled_pattern():
    """ignorecase in the dict comes from the compiled regex's flags, not the input bool."""
    spec = Specification(regex="abc", ignorecase=True)
    assert spec.regex.flags & re.IGNORECASE
    assert SpecificationSerializer.to_dict(spec)["ignorecase"] is True


def test_specification_serializer_to_json_none():
    assert SpecificationSerializer.to_json(None) == "null"


def test_specification_serializer_to_json_roundtrips_to_dict():
    spec = Specification(regex="abc", ignorecase=True, minlen=2)
    assert json.loads(SpecificationSerializer.to_json(spec)) == SpecificationSerializer.to_dict(spec)


def test_specification_serializer_to_json_forwards_kwargs():
    spec = Specification(regex="abc")
    output = SpecificationSerializer.to_json(spec, indent=2)
    assert "\n" in output
    assert json.loads(output) == SpecificationSerializer.to_dict(spec)


def _minimal_rule_dict():
    return {"id": "i", "group": "g", "message": "m", "severity": "s"}


def test_rule_serializer_to_dict_minimal():
    rule = Rule(_minimal_rule_dict())
    assert RuleSerializer.to_dict(rule) == {
        "id": "i",
        "group": "g",
        "message": "m",
        "severity": "s",
    }


def test_rule_serializer_to_dict_with_key():
    rule = Rule({**_minimal_rule_dict(), "key": {"regex": "k", "minlen": 2}})
    result = RuleSerializer.to_dict(rule)
    assert result["key"] == {"regex": "k", "ignorecase": False, "minlen": 2}
    assert "value" not in result


def test_rule_serializer_to_dict_with_value():
    rule = Rule({**_minimal_rule_dict(), "value": {"regex": "v"}})
    result = RuleSerializer.to_dict(rule)
    assert result["value"] == {"regex": "v", "ignorecase": False}
    assert "key" not in result


@pytest.mark.parametrize(
    ("similar", "expected_has_key", "expected_value"),
    [
        (1, False, None),
        (0.5, True, 0.5),
        (0, True, 0),
    ],
)
def test_rule_serializer_to_dict_similar(similar, expected_has_key, expected_value):
    rule = Rule({**_minimal_rule_dict(), "similar": similar})
    result = RuleSerializer.to_dict(rule)
    assert ("similar" in result) is expected_has_key
    if expected_has_key:
        assert result["similar"] == expected_value


def test_rule_serializer_to_dict_default_similar_omitted():
    """When `similar` isn't provided, Rule defaults it to 1 -> omitted from dict."""
    rule = Rule(_minimal_rule_dict())
    assert "similar" not in RuleSerializer.to_dict(rule)


def test_rule_serializer_round_trip():
    source = {
        "id": "secret-token",
        "group": "keys",
        "message": "Hard-coded secret token",
        "severity": "CRITICAL",
        "key": {"regex": "token|secret", "ignorecase": True, "minlen": 4},
        "value": {"regex": ".+", "minlen": 8, "isBase64": False},
        "similar": 0.8,
    }
    rule = Rule(source)
    serialized = RuleSerializer.to_dict(rule)
    restored = Rule(serialized)
    assert RuleSerializer.to_dict(restored) == serialized


def test_rule_serializer_to_json_parses_back_to_dict():
    rule = Rule({**_minimal_rule_dict(), "value": {"regex": "v"}, "similar": 0.5})
    assert json.loads(RuleSerializer.to_json(rule)) == RuleSerializer.to_dict(rule)


def test_rule_serializer_to_json_forwards_kwargs():
    rule = Rule(_minimal_rule_dict())
    output = RuleSerializer.to_json(rule, indent=2)
    assert "\n" in output
    assert json.loads(output) == RuleSerializer.to_dict(rule)


def test_rule_serializer_uses_fixture(rule_fixture):
    """The shared rule_fixture has empty {} key/value, which Rule._get_spec treats as falsy -> None."""
    result = RuleSerializer.to_dict(rule_fixture)
    assert result == {
        "id": "fixture",
        "group": "tests",
        "message": "test",
        "severity": "Info",
    }
