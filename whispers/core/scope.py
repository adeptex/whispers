from argparse import Namespace
from pathlib import Path
from typing import Iterator


def load_scope(args: Namespace, config: dict) -> Iterator[Path]:
    """Load a list of files in scope based on args and config"""
    src = Path(args.src)
    if src.is_file():
        yield src

    else:
        excluded = config.exclude.files
        for include in config.include.files:
            for path in src.rglob(include):
                if excluded and excluded.match(path.as_posix()):
                    continue

                yield path
