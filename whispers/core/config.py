import logging
from argparse import Namespace
from pathlib import Path

from whispers.core.utils import DEFAULT_PATH, load_yaml_from_file
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

    except Exception:
        raise RuntimeError(f"{configfile.as_posix()} is invalid")

    logging.debug(f"load_config '{config}'")
    return config
