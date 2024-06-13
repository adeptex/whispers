import pytest

from tests.unit.conftest import fixture_path
from whispers.core.args import parse_args
from whispers.main import main, run


def test_main():
    with pytest.raises(SystemExit):
        main()


@pytest.mark.parametrize(
    ("ast", "expected"),
    [
        ("--ast", 421),
        ("", 313),
    ],
)
def test_run(ast, expected):
    argv = ["-F", "None"]
    if ast:
        argv.append(ast)

    argv.append(fixture_path())
    args = parse_args(argv)
    secrets = list(run(args))
    assert len(secrets) == expected
