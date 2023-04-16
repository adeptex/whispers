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
    args = parse_args(["-S", "LOW", fixture_path(src)])
    config = load_config(args)
    rules = load_rules(args, config)
    pairs = make_pairs(config, FIXTURE_PATH.joinpath(src))
    result = list(map(lambda x: x.key, detect_secrets(rules, pairs)))
    assert set(result) == set(expected)


@pytest.mark.parametrize(
    ("src", "severity", "expected"),
    [
        (".aws/credentials", "CRITICAL", 3),
        (".dockercfg", "HIGH", 1),
        (".htpasswd", "MEDIUM", 2),
        (".npmrc", "HIGH", 5),
        (".pypirc", "HIGH", 1),
        ("apikeys-known.yml", "HIGH", 56),
        ("apikeys.json", "MEDIUM", 9),
        ("apikeys.xml", "MEDIUM", 9),
        ("apikeys.yml", "MEDIUM", 9),
        ("arn.yml", "LOW", 4),
        ("arn.xml", "LOW", 3),
        ("aws.yml", "CRITICAL", 3),
        ("aws.json", "CRITICAL", 3),
        ("aws.xml", "CRITICAL", 3),
        ("beans.xml", "HIGH", 1),
        ("beans.xml.dist", "HIGH", 1),
        ("beans.xml.template", "HIGH", 1),
        ("build.gradle", "HIGH", 2),
        ("cloudformation.json", "HIGH", 1),
        ("cloudformation.json.template", DEFAULT_SEVERITY, 0),
        ("cloudformation.yml", "HIGH", 1),
        # ("connection.config", "HIGH", 1),
        ("cors.py", "LOW", 1),
        ("creditcards.yml", "LOW", 3),
        ("custom.json", DEFAULT_SEVERITY, 0),
        ("custom.xml", DEFAULT_SEVERITY, 0),
        ("custom.yml", DEFAULT_SEVERITY, 0),
        ("Dockerfile", "MEDIUM", 3),
        ("empty.dockercfg", "CRITICAL,HIGH,MEDIUM,INFO", 0),
        ("excluded.json", "CRITICAL", 0),
        ("excluded.xml", "CRITICAL", 0),
        ("excluded.yml", "CRITICAL", 0),
        ("falsepositive.yml", DEFAULT_SEVERITY, 4),
        ("Groups.xml", "HIGH", 2),
        ("hardcoded.json", "HIGH", 5),
        ("hardcoded.xml", "HIGH", 5),
        ("hardcoded.yml", "HIGH", 5),
        ("integration.conf", "HIGH", 5),
        ("integration.json", "HIGH", 5),
        ("integration.xml", "HIGH", 5),
        ("integration.yml", "HIGH", 5),
        ("invalid.yml", DEFAULT_SEVERITY, 0),
        ("invalid.json", DEFAULT_SEVERITY, 0),
        ("invalid.ini", "CRITICAL,HIGH,MEDIUM,INFO", 0),
        ("invalid.py", DEFAULT_SEVERITY, 0),
        ("invalid.sh", DEFAULT_SEVERITY, 0),
        ("java.properties", "HIGH,MEDIUM", 3),
        ("jdbc.xml", "HIGH", 3),
        ("jenkins.xml", "HIGH,MEDIUM", 2),
        ("language.html", "INFO", 3),
        ("language.py", "HIGH", 11),
        ("language.py2", DEFAULT_SEVERITY, 0),
        ("language.sh", "HIGH,MEDIUM", 15),
        ("nginx.conf", DEFAULT_SEVERITY, 4),
        ("passwords.json", "HIGH", 5),
        ("passwords.xml", "HIGH", 5),
        ("passwords.yml", "HIGH", 5),
        ("paths.yml", DEFAULT_SEVERITY, 0),
        ("pip.conf", "HIGH", 2),
        ("placeholders.json", DEFAULT_SEVERITY, 0),
        ("placeholders.xml", DEFAULT_SEVERITY, 0),
        ("placeholders.yml", DEFAULT_SEVERITY, 0),
        ("plaintext.txt", "HIGH", 2),
        ("private-pgp-block.txt", "HIGH", 1),
        ("privatekey.pem", "HIGH", 1),
        ("privatekeys.json", "HIGH", 6),
        ("privatekeys.xml", "HIGH", 6),
        ("privatekeys.yml", "HIGH", 6),
        ("putty.ppk", DEFAULT_SEVERITY, 1),
        ("ruleslist.yml", "HIGH", 3),
        ("settings.cfg", "HIGH", 1),
        ("settings.conf", "HIGH", 1),
        ("settings.env", "HIGH", 1),
        ("settings01.ini", "HIGH", 1),
        ("settings02.ini", "HIGH", 1),
        ("severity.yml", "CRITICAL", 1),
        ("sops.yml", DEFAULT_SEVERITY, 1),
        ("uri.yml", "HIGH", 3),
        ("webhooks.yml", "LOW", 6),
    ],
)
def test_detect_secrets_by_value(src, severity, expected):
    args = parse_args(["--severity", severity, fixture_path(src)])
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
        ("language.html", 3, "comment"),
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
