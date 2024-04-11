import pytest

from tests.unit.conftest import fixture_path
from whispers.core.args import parse_args
from whispers.main import main, run


def test_main():
    with pytest.raises(SystemExit):
        main()


def test_run():
    argv = ["-F", "None", fixture_path()]
    args = parse_args(argv)
    secrets = list(run(args))
    assert len(secrets) == 325
