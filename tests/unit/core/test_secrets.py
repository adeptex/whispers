import pytest

from tests.unit.conftest import FIXTURE_PATH, config_path, fixture_path
from whispers.core.args import parse_args
from whispers.core.config import load_config
from whispers.core.constants import DEFAULT_SEVERITY
from whispers.core.pairs import make_pairs
from whispers.core.rules import load_rules
from whispers.core.secrets import detect_secrets, filter_rule
from whispers.core.utils import is_base64
from whispers.models.pair import KeyValuePair
from whispers.models.rule import Specification

DEFAULT_SEVERITY = ",".join(DEFAULT_SEVERITY)


def test_filter_rule_lineno(rule_fixture):
    pair = KeyValuePair("sonar.jdbc.password", "hardcoded02", file=FIXTURE_PATH.joinpath("java.properties"))
    rule_fixture.key = Specification(**{"regex": "sonar.*"})
    assert filter_rule(rule_fixture, pair).line == 10


@pytest.mark.parametrize(
    ("src", "expected"),
    [
        ("privatekeys.yml", ["access", "key", "rsa", "dsa", "ec", "openssh"]),
        ("privatekeys.json", ["access", "key", "rsa", "dsa", "ec", "openssh"]),
        ("privatekeys.xml", ["access", "key", "rsa", "dsa", "ec", "openssh"]),
        ("aws.yml", ["aws_id", "aws_key", "aws_token"]),
        ("aws.json", ["aws_id", "aws_key", "aws_token"]),
        ("aws.xml", ["aws_id", "aws_key", "aws_token"]),
        ("jenkins.xml", ["noncompliantApiToken", "noncompliantPasswordHash"]),
        ("cloudformation.yml", ["NoncompliantDBPassword"]),
        ("cloudformation.json", ["NoncompliantDBPassword"]),
    ],
)
def test_detect_secrets_by_key(src, expected):
    args = parse_args(["-S", "Low", fixture_path(src)])
    config = load_config(args)
    rules = load_rules(args, config)
    pairs = make_pairs(config, FIXTURE_PATH.joinpath(src))
    result = list(map(lambda x: x.key, detect_secrets(rules, pairs)))
    assert set(result) == set(expected)


@pytest.mark.parametrize(
    ("src", "severity", "expected"),
    [
        (".aws/credentials", "Critical", 3),
        (".dockercfg", "High", 1),
        (".htpasswd", "Medium", 2),
        (".npmrc", "High", 5),
        (".pypirc", "High", 1),
        ("apikeys-known.yml", "High", 56),
        ("apikeys.json", "Medium", 9),
        ("apikeys.xml", "Medium", 9),
        ("apikeys.yml", "Medium", 9),
        ("apikeys.json", "Low", 1),
        ("apikeys.xml", "Low", 2),
        ("apikeys.yml", "Low", 1),
        ("arn.yml", "Low", 4),
        ("arn.xml", "Low", 3),
        ("aws.yml", "Critical", 3),
        ("aws.yml", DEFAULT_SEVERITY, 7),
        ("aws.json", "Critical", 3),
        ("aws.json", DEFAULT_SEVERITY, 7),
        ("aws.xml", "Critical", 3),
        ("aws.xml", DEFAULT_SEVERITY, 7),
        ("beans.xml", "High", 1),
        ("beans.xml.dist", "High", 1),
        ("beans.xml.template", "High", 1),
        ("build.gradle", "High", 2),
        ("cloudformation.json", "High", 1),
        ("cloudformation.json.template", DEFAULT_SEVERITY, 0),
        ("cloudformation.yml", "High", 1),
        # ("connection.config", "High", 1),
        ("creditcards.yml", "Low", 3),
        ("custom.json", DEFAULT_SEVERITY, 0),
        ("custom.xml", DEFAULT_SEVERITY, 0),
        ("custom.yml", DEFAULT_SEVERITY, 0),
        ("Dockerfile", "Medium", 3),
        ("empty.dockercfg", "Critical,High,Medium,Info", 0),
        ("excluded.json", "Critical", 0),
        ("excluded.xml", "Critical", 0),
        ("excluded.yml", "Critical", 0),
        ("Groups.xml", "High", 2),
        ("hardcoded.json", "High", 5),
        ("hardcoded.xml", "High", 5),
        ("hardcoded.yml", "High", 5),
        ("integration.conf", "High", 5),
        ("integration.json", "High", 5),
        ("integration.xml", "High", 5),
        ("integration.yml", "High", 5),
        ("invalid.yml", DEFAULT_SEVERITY, 0),
        ("invalid.json", DEFAULT_SEVERITY, 0),
        ("invalid.ini", "Critical,High,Medium,Info", 0),
        ("invalid.py", DEFAULT_SEVERITY, 0),
        ("invalid.sh", DEFAULT_SEVERITY, 0),
        ("java.properties", "High,Medium", 3),
        ("jdbc.xml", "High", 3),
        ("jenkins.xml", "High,Medium", 2),
        ("nginx.conf", DEFAULT_SEVERITY, 4),
        ("page.html", "Info", 3),
        ("passwords.json", "High", 5),
        ("passwords.xml", "High", 5),
        ("passwords.yml", "High", 5),
        ("paths.yml", DEFAULT_SEVERITY, 0),
        ("pip.conf", "High", 2),
        ("placeholders.json", DEFAULT_SEVERITY, 0),
        ("placeholders.xml", DEFAULT_SEVERITY, 0),
        ("placeholders.yml", DEFAULT_SEVERITY, 0),
        ("plaintext.txt", "High", 2),
        ("private-pgp-block.txt", "High", 1),
        ("privatekey.pem", "High", 1),
        ("privatekeys.json", "High", 6),
        ("privatekeys.xml", "High", 6),
        ("privatekeys.yml", "High", 6),
        ("putty.ppk", DEFAULT_SEVERITY, 1),
        ("ruleslist.yml", "High", 3),
        ("script.sh", "High,Medium", 15),
        ("settings.cfg", "High", 1),
        ("settings.conf", "High", 1),
        ("settings.env", "High", 1),
        ("settings01.ini", "High", 1),
        ("settings02.ini", "High", 1),
        ("severity.yml", "Critical", 1),
        ("sops.yml", DEFAULT_SEVERITY, 1),
        ("uri.yml", "High", 4),
        ("webhooks.yml", "Low", 6),
        ("falsepositive/values.yml", DEFAULT_SEVERITY, 4),
        ("falsepositive/plain.txt", DEFAULT_SEVERITY, 0),
        ("falsepositive/semver.json", DEFAULT_SEVERITY, 0),
    ],
)
def test_detect_secrets_by_value(src, severity, expected):
    args = parse_args(["--ast", "--severity", severity, fixture_path(src)])
    config = load_config(args)
    rules = load_rules(args, config)
    pairs = make_pairs(config, FIXTURE_PATH.joinpath(src))
    result = detect_secrets(rules, pairs)
    count = 0

    for secret in result:
        count += 1

        if secret.value.isnumeric():
            continue

        if is_base64(secret.value):
            continue

        result = secret.value.lower()

        assert result.find("hardcoded") >= 0 or result.find("private key")

    assert count == expected


@pytest.mark.parametrize(
    ("expected"),
    [
        (".aws/credentials"),
        (".htpasswd"),
        (".npmrc"),
        (".pypirc"),
        ("connection.config"),
        ("integration.conf"),
        ("pip.conf"),
        ("settings.cfg"),
        ("settings.conf"),
        ("settings.env"),
        ("settings01.ini"),
    ],
)
def test_detect_secrets_by_filename(expected):
    args = parse_args(["-c", config_path("detection_by_filename.yml"), fixture_path(expected)])
    config = load_config(args)
    rules = load_rules(args, config)
    pairs = make_pairs(config, FIXTURE_PATH.joinpath(expected))
    result = map(lambda x: x.file, detect_secrets(rules, pairs))
    for item in result:
        assert item.endswith(expected)


@pytest.mark.parametrize(
    ("src", "count", "rule_id"),
    [
        ("page.html", 3, "comment"),
        ("passwords.json", 5, "password"),
    ],
)
def test_detect_secrets_by_rule(src, count, rule_id):
    args = parse_args(["--rules", rule_id, fixture_path(src)])
    config = load_config(args)
    rules = load_rules(args, config)
    pairs = make_pairs(config, FIXTURE_PATH.joinpath(src))
    result = list(map(lambda x: x.rule.id, detect_secrets(rules, pairs)))
    assert len(result) == count
    for item in result:
        assert item == rule_id
