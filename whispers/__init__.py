import shlex
from typing import Iterator

from whispers.core.args import parse_args
from whispers.core.utils import KeyValuePair
from whispers.main import run


def secrets(arguments: str) -> Iterator[KeyValuePair]:
    """
    Boilerplate for simplifying usage and integration.

    import whispers
    for secret in whispers.secrets("-r apikey path/to/source"):
        print(secret)
    """
    argv = shlex.split(arguments)
    return run(parse_args(argv))
