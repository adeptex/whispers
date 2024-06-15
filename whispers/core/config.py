import logging
from argparse import Namespace
from pathlib import Path
from sys import platform

from whispers.core.constants import DEFAULT_PATH
from whispers.core.utils import load_yaml_from_file
from whispers.models.appconfig import AppConfig


def load_config(args: Namespace) -> dict:
    """Load config given args"""
    if args.config:
        configfile = Path(args.config)
    else:
        configfile = DEFAULT_PATH.joinpath("config.yml")

    file_exists = False

    try:
        file_exists = configfile.exists()

    except OSError:  # pragma: no cover
        """
        Handle unpredictable file type situations.
        Example:
        Windows NUL behaves differently than Posix /dev/null.
        Doing os.stat(NUL) raises a system error, while
        os.stat(/dev/null) does not.
        """
        raise TypeError(f"{configfile.as_posix()} is not accessible")

    if not file_exists:
        raise FileNotFoundError(f"{configfile.as_posix()} does not exist")

    if not configfile.is_file():
        raise TypeError(f"{configfile.as_posix()} is not a file")

    try:
        config = AppConfig(load_yaml_from_file(configfile))
        config.ast = args.ast or config.ast
        config.ast ^= platform.startswith("win")  # Semgrep does not support Windows
        config.include.rules = args.rules or config.include.rules
        config.exclude.rules = args.xrules or config.exclude.rules
        config.include.groups = args.groups or config.include.groups
        config.exclude.groups = args.xgroups or config.exclude.groups
        config.include.severity = args.severity or config.include.severity
        config.exclude.severity = args.xseverity or config.exclude.severity
        config.include.files = args.files or config.include.files
        config.exclude.files = args.xfiles or config.exclude.files

    except Exception:
        raise RuntimeError(f"{configfile.as_posix()} is invalid")

    logging.debug(f"load_config '{config}'")
    return config
