import json
from io import StringIO
from unittest.mock import patch

import pytest

from tests.unit.conftest import fixture_path
from whispers.core.args import parse_args
from whispers.main import run


@pytest.mark.parametrize(
    ("srcfile", "expected"),
    [
        ("build.gradle.kts", 1),
        ("fixture.c", 5),
        ("fixture.cpp", 5),
        ("fixture.cs", 7),
        ("fixture.go", 9),
        ("fixture.java", 4),
        ("fixture.js", 10),
        ("fixture.kts", 5),
        ("fixture.lua", 5),
        ("fixture.php", 8),
        ("fixture.py", 10),
        ("fixture.rb", 9),
        ("fixture.scala", 8),
        ("fixture.ts", 11),
        ("fixture.vue", 11),
    ],
)
def test_pairs(srcfile, expected):
    testfile = fixture_path(f"ast/{srcfile}")
    args = parse_args(["--ast", "-F", "None", testfile])
    result = list(run(args))
    assert len(result) == expected
    assert all(["hardcoded" in pair.value.lower() for pair in result])


@pytest.mark.parametrize(
    ("srcfile", "expected"),
    [
        ("build.gradle.kts", 1),
        ("404.c", 0),
    ],
)
def test_ast_dump(srcfile, expected):
    testfile = fixture_path(f"ast/{srcfile}")
    mock_print = StringIO()

    with patch("sys.stdout", mock_print):
        with pytest.raises(SystemExit):
            parse_args(["--dump", testfile])

        result = json.loads(mock_print.getvalue())
        assert len(result) == expected
