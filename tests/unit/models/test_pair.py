from whispers.models.pair import KeyValuePair


def test_pair():
    pair = KeyValuePair("key", "value", ["key", "path"], "file", 123, {"rule_id": "test"})
    assert pair.__dict__ == {
        "key": "key",
        "value": "value",
        "keypath": ["key", "path"],
        "file": "file",
        "line": 123,
        "rule": {"rule_id": "test"},
    }


def test_pair_post_init():
    pair = KeyValuePair("key", "value")
    assert pair.keypath == ["key"]


# def test_printer_json(tmp_path, rule_fixture):
#     tmp = tmp_path.joinpath("printer.test")
#     args = parse_args(["-o", tmp.as_posix(), fixture_path()])
#     pair = KeyValuePair("key", "value", ["root", "key"], "/file", 123, rule_fixture)
#     expected = {
#         "key": pair.key,
#         "value": pair.value,
#         "file": pair.file,
#         "line": pair.line,
#         "rule_id": pair.rule.id,
#         "message": pair.rule.message,
#         "severity": pair.rule.severity,
#     }
#     result = json.loads(printer(args, pair))

#     assert result == expected
