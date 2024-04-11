from pathlib import Path
from typing import Iterator

from whispers.models.pair import KeyValuePair


class Elixir:
    def pairs(self, filepath: Path) -> Iterator[KeyValuePair]:
        for lineno, line in enumerate(filepath.open(), 1):
            for statement in line.split(","):
                if ": " not in statement:
                    continue

                key, value = statement.split(": ")
                yield KeyValuePair(key, value, line=lineno)
