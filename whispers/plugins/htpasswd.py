from pathlib import Path
from typing import Iterator

from whispers.core.utils import strip_string
from whispers.models.pair import KeyValuePair


class Htpasswd:
    def pairs(self, filepath: Path) -> Iterator[KeyValuePair]:
        for lineno, line in enumerate(filepath.open(), 1):
            if ":" not in line:
                continue

            creds = line.strip().split(":")
            value = strip_string(creds[1])
            if value:
                key = "htpasswd hash"
                yield KeyValuePair(key, value, line=lineno)
