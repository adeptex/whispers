from pathlib import Path
from typing import Iterator

from whispers.models.pair import KeyValuePair


class Gradle:
    def pairs(self, filepath: Path) -> Iterator[KeyValuePair]:
        key = "password"

        for lineno, line in enumerate(filepath.open(), 1):
            line = line.strip()

            if key not in line:
                continue

            value = line.split(key)[-1].strip(":) ")
            if value:
                yield KeyValuePair(key, value, line=lineno)
