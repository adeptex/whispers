from configparser import ConfigParser, MissingSectionHeaderError
from itertools import chain
from pathlib import Path
from typing import Iterator, Optional

from whispers.core.utils import strip_string
from whispers.models.pair import KeyValuePair
from whispers.plugins.xml import Xml


class Config:
    def pairs(self, filepath: Path) -> Iterator[KeyValuePair]:
        if "<?xml " in filepath.open("r").readline():
            yield from Xml().pairs(filepath)

        else:
            try:
                # Attempt to parse as Windows INI
                yield from self.parse_as_ini(filepath)

            except MissingSectionHeaderError:
                # Otherwise, parse as text line by line
                yield from self.parse_as_text(filepath)

    @staticmethod
    def parse_as_ini(filepath: Path) -> Optional[KeyValuePair]:
        parser = ConfigParser()
        parser.read(filepath.as_posix())
        sections = map(lambda section: section.items(), parser.values())
        items = chain.from_iterable(sections)

        for item in items:
            key, value = item
            yield KeyValuePair(key, value)

    @staticmethod
    def parse_as_text(filepath: Path) -> Optional[KeyValuePair]:
        for lineno, line in enumerate(filepath.open(), 1):
            line = line.strip()
            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = strip_string(key)
            value = strip_string(value)

            if value:
                yield KeyValuePair(key, value, line=lineno)
