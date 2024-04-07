import re
from pathlib import Path

import pytest
from yaml import safe_load
from yaml.parser import ParserError

from tests.unit.conftest import CONFIG_PATH, does_not_raise, fixture_path
from whispers.core.args import parse_args
from whispers.core.utils import (
    default_rules,
    find_line_number,
    is_ascii,
    is_base64,
    is_base64_bytes,
    is_iac,
    is_luhn,
    is_path,
    is_semver,
    is_static,
    is_uri,
    list_rule_prop,
    load_regex,
    load_yaml_from_file,
    similar_strings,
    simple_string,
    strip_string,
    truncate_all_space,
)
from whispers.main import run
from whispers.models.pair import KeyValuePair


@pytest.mark.parametrize(
    ("rawstr", "expected", "raised"),
    [
        ("test", re.compile("test"), does_not_raise()),
        ("*", None, pytest.raises(ValueError)),
        (".*", re.compile(".*"), does_not_raise()),
    ],
)
def test_load_regex(rawstr, expected, raised):
    with raised:
        assert load_regex(rawstr) == expected


@pytest.mark.parametrize(
    ("rawstr", "expected"),
    [
        ("", ""),
        ("whis\npers", "whis pers"),
        ("whis\tpers", "whis pers"),
        ("whis\n\n\n\npers", "whis pers"),
        ("whis\n       pers", "whis pers"),
    ],
)
def test_truncate_all_space(rawstr, expected):
    assert truncate_all_space(rawstr) == expected


@pytest.mark.parametrize(
    "rawstr",
    [
        "'whispers'",
        "\"'whispers'\"",
        "''whispers\"",
        "whispers\n\n",
        "\t\twhispers",
        "whispers\r\n",
        '    \t\'whispers""\r\n',
    ],
)
def test_strip_string(rawstr):
    assert strip_string(rawstr) == "whispers"


@pytest.mark.parametrize(
    ("rawstr", "expected"),
    [
        (None, ""),
        (1, "1"),
        ("~|wHisP3R5~|", "__whisp3r5__"),
    ],
)
def test_simple_string(rawstr, expected):
    assert simple_string(rawstr) == expected


@pytest.mark.parametrize(
    ("str1", "str2", "expected"),
    [
        ("whispers", "WHISPERS!!!", True),
        ("W h  I S P e r s", "WHISPERS!!!", True),
        ("AAAAAAA", "WHISPERS!!!", False),
    ],
)
def test_similar_strings(str1, str2, expected):
    assert bool(similar_strings(str1, str2)) is expected


@pytest.mark.parametrize(
    ("src", "key", "value", "expected"),
    [
        ("apikeys.yml", "apikey", "YXNkZmZmZmZm_HARDcoded", 11),
        ("apikeys.yml", "GITHUBKEY", "YXNkZmZmZmZm_HARDcoded", 19),
        ("pip.conf", "username", "hardcoded1", 7),
        ("java.properties", "sonar.jdbc.password", "hardcoded02", 10),
    ],
)
def test_find_line_number_single(src, key, value, expected):
    pair = KeyValuePair(key, value, keypath=[key, value], file=fixture_path(src))
    assert find_line_number(pair) == expected


@pytest.mark.parametrize(
    ("src", "linenumbers"),
    [
        ("hardcoded.yml", [12, 14, 15, 16, 19]),
        ("privatekeys.yml", [5, 7, 11, 12, 13, 14]),
        ("java.properties", [9, 10, 11]),
    ],
)
def test_find_line_number_all(src, linenumbers):
    args = parse_args([fixture_path(src)])
    secrets = run(args)
    for number in linenumbers:
        assert next(secrets).line == number


@pytest.mark.parametrize(
    ("configfile", "expected", "raised"),
    [
        ("example.yml", safe_load(CONFIG_PATH.joinpath("example.yml").read_text()), does_not_raise()),
        ("invalid.yml", {}, pytest.raises(ParserError)),
    ],
)
def test_load_yaml_from_file(configfile, expected, raised):
    with raised:
        result = load_yaml_from_file(CONFIG_PATH.joinpath(configfile))
        assert result == expected


@pytest.mark.parametrize(
    ("key", "value", "expected"),
    [
        (None, None, False),
        ("key", "", False),
        ("key", "$value", True),
        ("key", "$$Value", True),
        ("key", "$VALUE", False),
        ("key", "${value}", False),
        ("key", "${VALUE}", False),
        ("key", "{{value}}", False),
        ("key", "{value}", False),
        ("key", "{whispers~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~}", False),
        ("key", "{d2hpc3BlcnN+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+}", True),
        ("key", "${value$}", False),
        ("key", "<value>", False),
        ("key", "{value}", False),
        ("key", "null", False),
        ("key", "!Ref Value", False),
        ("key", "{value}", False),
        ("key", "/system/path/value", False),
        ("thesame", "THESAME", False),
        ("label", "WhispersLabel", False),
        ("_key", "-key", False),
        ("_secret_value_placeholder_", "----SECRET-VALUE-PLACEHOLDER-", False),
        ("_secret_value_placeholder_", "----SECRET-VALUE-PLACEHOLDER--", True),
        ("SECRET_VALUE_KEY", "whispers", True),
        ("whispers", "SECRET_VALUE_PLACEHOLDER", True),
        ("secret", "whispers", True),
    ],
)
def test_is_static(key, value, expected):
    assert is_static(key, value) == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        ("whispers", True),
        (b"whispers", True),
        (1234, True),
        (type(None), False),
        (".,:R*!#&_", True),
        (b"\xcc", False),
        ("\xcc", False),
        ("\u0041", True),
        ("\u5341", False),
    ],
)
def test_is_ascii(data, expected):
    assert is_ascii(data) == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        ("whispers", False),
        ("d2hpc3BlcnMK", True),
        (1234, False),
        (type(None), False),
        (".,:R*!#&_", False),
        (b"\xcc", False),
        ("\xcc", False),
        ("\u0041", False),
        ("\u5341", False),
    ],
)
def test_is_base64(data, expected):
    assert is_base64(data) == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        ("whispers", True),
        ("d2hpc3BlcnMK", True),
        (1234, False),
        (type(None), False),
        (".,:R*!#&_", False),
        (b"\xcc", False),
        ("\xcc", False),
        ("\u0041", False),
        ("\u5341", False),
    ],
)
def test_is_base64_bytes(data, expected):
    assert is_base64_bytes(data) == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        ("whispers", False),
        ("http://", False),
        ("http://user:pass@localhost.localdomain", True),
        (1234, False),
        (type(None), False),
        (".,:R*!#&_", False),
        (b"\xcc", False),
        ("\xcc", False),
        ("\u0041", False),
        ("\u5341", False),
    ],
)
def test_is_uri(data, expected):
    assert is_uri(data) == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        ("whispers", False),
        ("C:\\Windows", True),
        ("file:///home/user", True),
        ("root:///var/log/nginx", True),
        (1234, False),
        (type(None), False),
        (".,:R*!#&_", False),
        (b"\xcc", False),
        ("\xcc", False),
        ("\u0041", False),
        ("\u5341", False),
    ],
)
def test_is_path(data, expected):
    assert is_path(data) == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        ("whispers", False),
        ("!Ref Whispers", True),
        (1234, False),
        (type(None), False),
        (".,:R*!#&_", False),
        (b"\xcc", False),
        ("\xcc", False),
        ("\u0041", False),
        ("\u5341", False),
    ],
)
def test_is_iac(data, expected):
    assert is_iac(data) == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        ("whispers", False),
        (4111111111111111, True),
        (4111111111111112, False),
        (1234, False),
        (type(None), False),
        (".,:R*!#&_", False),
        (b"\xcc", False),
        ("\xcc", False),
        ("\u0041", False),
        ("\u5341", False),
    ],
)
def test_is_luhn(data, expected):
    assert is_luhn(data) == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        ("a.a.a", False),
        ("1,2,3", False),
        ("1.2.3", True),
        ("^1.2.3", True),
        ("v1.2.3", True),
        ("==1.2", True),
        (">=1.2", True),
    ],
)
def test_is_semver(data, expected):
    assert is_semver(data) == expected


def test_default_rules():
    rules = default_rules()
    rule_files = Path("whispers/rules").glob("*.yml")
    rule_yaml = map(load_yaml_from_file, rule_files)
    rule_items = (rule for rules in rule_yaml for rule in rules)

    for rule in rule_items:
        assert rule["id"] in rules


def test_list_rule_prop():
    rule = {"id": "rule-id"}
    assert list_rule_prop("id", [rule]) == ["rule-id"]
