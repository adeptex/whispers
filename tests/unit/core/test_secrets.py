import pytest

from tests.unit.conftest import FIXTURE_PATH, config_path, fixture_path
from whispers.core.args import parse_args
from whispers.core.config import load_config
from whispers.core.pairs import make_pairs
from whispers.core.rules import load_rules
from whispers.core.secrets import detect_secrets, filter_rule
from whispers.core.utils import DEFAULT_SEVERITY, is_base64
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
    args = parse_args([fixture_path(src)])
    config = load_config(args)
    rules = load_rules(args, config)
    pairs = make_pairs(config, FIXTURE_PATH.joinpath(src))
    result = list(map(lambda x: x.key, detect_secrets(rules, pairs)))
    assert set(result) == set(expected)


@pytest.mark.parametrize(
    ("src", "severity", "expected"),
    [
        (".aws/credentials", "BLOCKER", 3),
        (".dockercfg", "CRITICAL", 1),
        (".htpasswd", "MAJOR", 2),
        (".npmrc", "CRITICAL", 3),
        (".pypirc", "CRITICAL", 1),
        ("apikeys-known.yml", "CRITICAL", 54),
        ("apikeys.json", "MAJOR", 9),
        ("apikeys.xml", "MAJOR", 9),
        ("apikeys.yml", "MAJOR", 9),
        ("aws.yml", "BLOCKER", 3),
        ("aws.json", "BLOCKER", 3),
        ("aws.xml", "BLOCKER", 3),
        ("beans.xml", "CRITICAL", 1),
        ("beans.xml.dist", "CRITICAL", 1),
        ("beans.xml.template", "CRITICAL", 1),
        ("build.gradle", "CRITICAL", 2),
        ("cloudformation.json", "CRITICAL", 1),
        ("cloudformation.json.template", DEFAULT_SEVERITY, 0),
        ("cloudformation.yml", "CRITICAL", 1),
        # ("connection.config", "CRITICAL", 1),
        ("cors.py", "MINOR", 1),
        ("creditcards.yml", "MINOR", 3),
        ("custom.json", DEFAULT_SEVERITY, 0),
        ("custom.xml", DEFAULT_SEVERITY, 0),
        ("custom.yml", DEFAULT_SEVERITY, 0),
        ("Dockerfile", "MAJOR", 3),
        ("empty.dockercfg", "BLOCKER,CRITICAL,MAJOR,INFO", 0),
        ("excluded.json", "BLOCKER", 0),
        ("excluded.xml", "BLOCKER", 0),
        ("excluded.yml", "BLOCKER", 0),
        ("falsepositive.yml", DEFAULT_SEVERITY, 4),
        ("Groups.xml", "CRITICAL", 2),
        ("hardcoded.json", "CRITICAL", 5),
        ("hardcoded.xml", "CRITICAL", 5),
        ("hardcoded.yml", "CRITICAL", 5),
        ("integration.conf", "CRITICAL", 5),
        ("integration.json", "CRITICAL", 5),
        ("integration.xml", "CRITICAL", 5),
        ("integration.yml", "CRITICAL", 5),
        ("invalid.yml", DEFAULT_SEVERITY, 0),
        ("invalid.json", DEFAULT_SEVERITY, 0),
        ("invalid.ini", "BLOCKER,CRITICAL,MAJOR,INFO", 0),
        ("invalid.py", DEFAULT_SEVERITY, 0),
        ("invalid.sh", DEFAULT_SEVERITY, 0),
        ("java.properties", "CRITICAL,MAJOR", 3),
        ("jdbc.xml", "CRITICAL", 3),
        ("jenkins.xml", "CRITICAL,MAJOR", 2),
        ("language.html", "INFO", 3),
        ("language.py", "CRITICAL", 11),
        ("language.py2", DEFAULT_SEVERITY, 0),
        ("language.sh", "CRITICAL,MAJOR", 14),
        ("passwords.json", "CRITICAL", 5),
        ("passwords.xml", "CRITICAL", 5),
        ("passwords.yml", "CRITICAL", 5),
        ("paths.yml", DEFAULT_SEVERITY, 0),
        ("pip.conf", "CRITICAL", 2),
        ("placeholders.json", DEFAULT_SEVERITY, 0),
        ("placeholders.xml", DEFAULT_SEVERITY, 0),
        ("placeholders.yml", DEFAULT_SEVERITY, 0),
        ("plaintext.txt", "CRITICAL", 2),
        ("private-pgp-block.txt", "CRITICAL", 1),
        ("privatekey.pem", "CRITICAL", 1),
        ("privatekeys.json", "CRITICAL", 6),
        ("privatekeys.xml", "CRITICAL", 6),
        ("privatekeys.yml", "CRITICAL", 6),
        ("putty.ppk", DEFAULT_SEVERITY, 1),
        ("ruleslist.yml", "CRITICAL", 3),
        ("settings.cfg", "CRITICAL", 1),
        ("settings.conf", "CRITICAL", 1),
        ("settings.env", "CRITICAL", 1),
        ("settings01.ini", "CRITICAL", 1),
        ("settings02.ini", "CRITICAL", 1),
        ("severity.yml", "BLOCKER", 1),
        ("sops.yml", DEFAULT_SEVERITY, 1),
        ("uri.yml", "CRITICAL", 3),
        ("webhooks.yml", "MINOR", 6),
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
    ("src", "count", "rule_id"), [("language.html", 3, "comment"), ("passwords.json", 5, "password"),],
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
