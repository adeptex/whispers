import pytest

import whispers
from tests.unit.conftest import config_path, fixture_path


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        (f"-c {config_path('integration.yml')} {fixture_path()}", 3),
        (f"-r apikey-known {fixture_path('apikeys-known.yml')}", 54),
        (f"--rules sensitive {fixture_path('files')}", 3),
        (f"-s BLOCKER {fixture_path('aws.yml')}", 3),
    ],
)
def test_whispers(args, expected):
    result = list(whispers.secrets(args))
    assert len(result) == expected
