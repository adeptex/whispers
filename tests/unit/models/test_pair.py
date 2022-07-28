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
