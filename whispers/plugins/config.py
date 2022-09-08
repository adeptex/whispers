from configparser import ConfigParser, MissingSectionHeaderError
from itertools import chain
from pathlib import Path
from typing import Iterator, Optional

from crossplane import parse as nginx_parse

from whispers.core.utils import strip_string
from whispers.models.pair import KeyValuePair
from whispers.plugins.common import Common
from whispers.plugins.traverse import StructuredDocument
from whispers.plugins.xml import Xml


class Config:
    def pairs(self, filepath: Path) -> Iterator[KeyValuePair]:
        if "<?xml " in filepath.open("r").readline():
            yield from Xml().pairs(filepath)

        else:
            # Attempt to parse as Nginx config
            yield from self.parse_as_nginx(filepath)

            try:
                # Attempt to parse as Windows INI
                yield from self.parse_as_ini(filepath)

            except MissingSectionHeaderError:
                # Otherwise, parse as text line by line
                yield from self.parse_as_text(filepath)

    @staticmethod
    def parse_as_ini(filepath: Path) -> Optional[KeyValuePair]:
        """Parse file as Windows .ini"""
        parser = ConfigParser()
        parser.read(filepath.as_posix())
        sections = map(lambda section: section.items(), parser.values())
        items = chain.from_iterable(sections)

        for item in items:
            key, value = item
            yield KeyValuePair(key, value)

    @staticmethod
    def parse_as_text(filepath: Path) -> Optional[KeyValuePair]:
        """Parse as plain text"""
        for lineno, line in enumerate(filepath.open(), 1):
            line = line.strip()
            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = strip_string(key)
            value = strip_string(value)

            if value:
                yield KeyValuePair(key, value, line=lineno)

    @staticmethod
    def parse_as_nginx(filepath: Path) -> Optional[Iterator[KeyValuePair]]:
        """Parse file as nginx.conf"""
        nginx_conf = nginx_parse(filepath, strict=False, single=True)
        if nginx_conf.get("status") != "ok":
            return  # skip failed (ie: not nginx.conf format)

        pairs = StructuredDocument().traverse(nginx_conf)
        args = filter(lambda pair: pair.key == "args", pairs)

        while True:
            try:
                key = next(args).value
                value = next(args).value
                keypath = [key, value]
                yield KeyValuePair(key, value, keypath, filepath.as_posix())
                yield from Common(keypath).parse_uri(value)

            except Exception:
                return
