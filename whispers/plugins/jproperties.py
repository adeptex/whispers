from pathlib import Path
from typing import Iterator

from jproperties import Properties

from whispers.models.pair import KeyValuePair


class Jproperties:
    def pairs(self, filepath: Path) -> Iterator[KeyValuePair]:
        props = Properties()
        props.load(filepath.read_text(), "utf-8")
        for key, value in props.properties.items():
            yield KeyValuePair(key, value, [key])
