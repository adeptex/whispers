import pytest

from tests.unit.conftest import fixture_path
from whispers.core.args import parse_args
from whispers.main import main, run


def test_main():
    with pytest.raises(SystemExit):
        main()


def test_run():
    args = parse_args([fixture_path()])
    secrets = list(run(args))
    assert len(secrets) == 322
