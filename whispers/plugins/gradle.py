from pathlib import Path
from typing import Iterator

from whispers.core.utils import KeyValuePair


class Gradle:
    def pairs(self, filepath: Path) -> Iterator[KeyValuePair]:
        for lineno, line in enumerate(filepath.open(), 1):
            line = line.strip()
            if "authentication(" not in line:
                continue

            key = "password"

            if f"{key}:" not in line:
                continue

            value = line.split(f"{key}:")[-1].strip(") ")

            if value:
                yield KeyValuePair(key, value, keypath=["authentication", key], line=lineno)
