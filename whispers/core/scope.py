from argparse import Namespace
from pathlib import Path
from typing import Iterable


def load_scope(args: Namespace, config: dict) -> Iterable[Path]:
    """Load a list of files in scope based on args and config"""
    include_files = args.files or config.include.files
    exclude_files = args.xfiles or config.exclude.files
    src = Path(args.src)

    if src.is_file():
        yield src

    else:
        for include in include_files:
            for filepath in src.rglob(include):
                if exclude_files and exclude_files.match(filepath.as_posix()):
                    continue

                yield filepath
