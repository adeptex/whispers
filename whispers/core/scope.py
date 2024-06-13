from argparse import Namespace
from pathlib import Path
from typing import Iterable


def load_scope(args: Namespace, config: dict) -> Iterable[Path]:
    """Load a list of files in scope based on args and config"""
    src = Path(args.src)

    if src.is_file():
        yield src

    else:
        for include in config.include.files:
            for filepath in src.rglob(include):
                if config.exclude.files and config.exclude.files.match(filepath.as_posix()):
                    continue

                yield filepath
