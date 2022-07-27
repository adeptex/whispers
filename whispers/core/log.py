import logging
import logging.config
from argparse import Namespace
from pathlib import Path
from tempfile import gettempdir
from typing import Optional


def global_exception_handler(file: str, data: str):
    logging.exception(f"File: {file}\n{data}")
