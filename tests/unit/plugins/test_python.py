from datetime import datetime
from os import remove

import astroid
import pytest
from astroid.nodes import AssignName, Const, JoinedStr, Name

from tests.unit.conftest import FIXTURE_PATH, does_not_raise
from whispers.plugins.python import Python


@pytest.mark.parametrize(
    ("code", "exception"),
    [
        ("a=1", does_not_raise()),
        ("invalid:", pytest.raises(StopIteration)),
    ],
)
def test_pairs(code, exception):
    stamp = datetime.now().timestamp()
    testfile = FIXTURE_PATH.joinpath(f"test-{stamp}.py")
    testfile.write_text(code)
    plugin = Python()
    with exception:
        try:
            next(plugin.pairs(testfile))
        except Exception:
            raise
        finally:
            remove(testfile.as_posix())


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        (None, False),
        (True, False),
        (1, False),
        ("test", False),
        (Name("test", 1, 0, None, end_lineno=0, end_col_offset=0), True),
        (AssignName("test"), True),
        (Const("test"), False),
        (JoinedStr("test"), False),
    ],
)
def test_is_key(key, expected):
    plugin = Python()
    assert plugin.is_key(key) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, False),
        (True, False),
        (1, False),
        ("test", False),
        (Name("test", 1, 0, None, end_lineno=0, end_col_offset=0), False),
        (AssignName("test"), False),
        (Const("test"), True),
        (JoinedStr("test"), True),
    ],
)
def test_is_value(value, expected):
    plugin = Python()
    assert plugin.is_value(value) == expected


@pytest.mark.parametrize(
    ("code", "key", "value", "exception"),
    [
        ("a=1", "a", 1, does_not_raise()),
        ("a='b'", "a", "b", does_not_raise()),
        ("a=b", "", "", pytest.raises(StopIteration)),
        ("a==1", "a", 1, does_not_raise()),
        ("a=='b'", "a", "b", does_not_raise()),
        ("'b'==a", "a", "b", does_not_raise()),
        ("a==b", "", "", pytest.raises(StopIteration)),
        ("a==''", "", "", pytest.raises(StopIteration)),
        ("{'a': 1}", "a", 1, does_not_raise()),
        ("{'a': 'b'}", "a", "b", does_not_raise()),
        ("{'a': ''}", "", "", pytest.raises(StopIteration)),
    ],
)
def test_traverse_parse(code, key, value, exception):
    plugin = Python()
    ast = astroid.parse(code)
    pairs = plugin.traverse(ast)
    with exception:
        pair = next(pairs)
        assert pair.key == key
        assert pair.value == value


@pytest.mark.parametrize(
    ("code", "key", "value", "exception"),
    [
        ("callback(a=1)", "a", 1, does_not_raise()),
        ("callback(a='b')", "a", "b", does_not_raise()),
        ("callback(a='')", "", "", pytest.raises(StopIteration)),
        ("a=os.getenv('b')", "function", "os.getenv('b')", does_not_raise()),
    ],
)
def test_traverse_extract(code, key, value, exception):
    plugin = Python()
    ast = astroid.extract_node(code)
    pairs = plugin.traverse(ast)
    with exception:
        pair = next(pairs)
        assert pair.key == key
        assert pair.value == value
