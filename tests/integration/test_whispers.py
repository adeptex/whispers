import pytest

import whispers
from tests.unit.conftest import config_path, fixture_path


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        (f"-c {config_path('integration.yml')} {fixture_path()}", 5),
        (f"-r apikey-known {fixture_path('apikeys-known.yml')}", 56),
        (f"--rules file-known {fixture_path('files')}", 3),
        (f"-s Critical {fixture_path('aws.yml')}", 3),
    ],
)
def test_whispers(args, expected):
    result = list(whispers.secrets(args))
    assert len(result) == expected


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        ("-f '*json'", ("json",)),
        ("-f '*yml'", ("yml",)),
        ("-f '*json,*yml'", ("json", "yml")),
    ],
)
def test_glob_filter(args, expected):
    args = f"{args} {fixture_path()}"
    for secret in whispers.secrets(args):
        assert secret.file.endswith(expected)


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        ("-F '.*json'", ("json",)),
        ("-F '.*yml'", ("yml",)),
        ("-F '.*(json|yml)'", ("json", "yml")),
    ],
)
def test_regex_filter(args, expected):
    args = f"{args} {fixture_path()}"
    for secret in whispers.secrets(args):
        assert not secret.file.endswith(expected)
