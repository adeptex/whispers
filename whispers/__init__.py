from typing import Iterator


def secrets(arguments: str) -> Iterator:
    """
    Boilerplate for simplifying usage and integration.

    import whispers
    for secret in whispers.secrets("-r apikey tests/fixtures"):
        print(secret)
    """
    import shlex

    from whispers.core.args import parse_args
    from whispers.main import run

    argv = shlex.split(arguments)
    return run(parse_args(argv))
