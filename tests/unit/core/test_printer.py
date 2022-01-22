import json

from tests.unit.conftest import fixture_path
from whispers.core.args import parse_args
from whispers.core.printer import printer
from whispers.models.pair import KeyValuePair


def test_printer_json(tmp_path, rule_fixture):
    tmp = tmp_path.joinpath("printer.test")
    args = parse_args(["-o", tmp.as_posix(), fixture_path()])
    pair = KeyValuePair("key", "value", ["root", "key"], "/file", 123, rule_fixture)
    expected = {
        "key": pair.key,
        "value": pair.value,
        "file": pair.file,
        "line": pair.line,
        "rule_id": pair.rule.id,
        "message": pair.rule.message,
        "severity": pair.rule.severity,
    }
    result = json.loads(printer(args, pair))

    assert result == expected


def test_printer_human(rule_fixture):
    args = parse_args(["-H", fixture_path()])
    pair = KeyValuePair("key", "value", ["root", "key"], "/file", 123, rule_fixture)
    expected = (
        f"[{pair.file}:{pair.line}:{pair.rule.group}:{pair.rule.id}:{pair.rule.severity}]"
        + f" {pair.key} = {pair.value}"
    )
    result = printer(args, pair)

    assert result == expected
