import pytest

from whispers.plugins.common import Common


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", None),
        (123, None),
        ("jdbc:mysql://localhost/authority?userpass=hardcoded0", "hardcoded0"),
        ("arn:aws:kms:eu-central-1:123456123456:key/hardcoded", "123456123456"),
    ],
)
def test_pairs(text, expected):
    plugin = Common()
    for pair in plugin.pairs(text):
        assert pair.value == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("http", None),
        ("jdbc:mysql://localhost/authority?userpass=hardcoded0", "hardcoded0"),
        ("jdbc:mysql://localhost/authority?user=&userpass=", None),
        ("amqp://root:hardcoded2@localhost.local:5434/topic", "root:hardcoded2"),
        ("amqp://root@localhost.local:5434/topic", None),
        ("amqp://localhost.local:5434/topic", None),
    ],
)
def test_parse_uri(text, expected):
    plugin = Common()
    for pair in plugin.parse_uri(text):
        assert pair.value == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("invalid:", None),
        ("arn:aws:kms:eu-central-1", None),
        ("arn:aws:kms:eu-central-1:", None),
        ("arn:aws:kms:eu-central-1:123456123456:key/hardcoded", "123456123456"),
    ],
)
def test_parse_arn(text, expected):
    plugin = Common()
    for pair in plugin.parse_arn(text):
        assert pair.value == expected
