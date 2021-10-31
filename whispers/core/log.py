import logging
import logging.config
from argparse import Namespace
from pathlib import Path
from tempfile import gettempdir
from typing import Optional


def configure_log(args: Namespace) -> Optional[Path]:
    """Configure logging"""
    if not args.log:
        logging.getLogger().setLevel(logging.CRITICAL)
        return None

    logpath = Path(gettempdir()).joinpath("whispers.log")
    logpath.write_text("")

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "class": "logging.Formatter",
                    "style": "{",
                    "datefmt": "%Y-%m-%d %H:%M",
                    "format": "[{asctime:s}] {message:s}",
                }
            },
            "handlers": {
                "default": {
                    "level": args.debug,
                    "class": "logging.handlers.WatchedFileHandler",
                    "formatter": "default",
                    "filename": logpath.as_posix(),
                    "mode": "w",
                    "encoding": "utf-8",
                }
            },
            # root logger
            "loggers": {"": {"handlers": ["default"], "level": args.debug, "propagate": False}},
        }
    )

    return logpath


def global_exception_handler(file: str, data: str):
    logging.exception(f"File: {file}\n{data}")
