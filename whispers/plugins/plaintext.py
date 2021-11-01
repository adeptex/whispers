from pathlib import Path
from typing import Iterator, Optional

from whispers.core.utils import is_uri, strip_string
from whispers.models.pair import KeyValuePair
from whispers.plugins.uri import Uri


class Plaintext:
    def pairs(self, filepath: Path) -> Iterator[KeyValuePair]:
        for lineno, line in enumerate(filepath.open(), 1):
            line = strip_string(line)
            if not line:
                continue

            yield from self.uri_pairs(line, lineno)
            yield from self.privatekey_pairs(line, lineno)

    @staticmethod
    def privatekey_pairs(line: str, lineno: int) -> Optional[Iterator[KeyValuePair]]:
        if not (line.startswith("---") and line.endswith("---")):
            return None

        if len(line) < 12:
            return None

        yield KeyValuePair("key", line, line=lineno)

    @staticmethod
    def uri_pairs(line: str, lineno: int) -> Optional[Iterator[KeyValuePair]]:
        if "://" not in line:
            return None

        for value in line.split():
            if not is_uri(value):
                continue

            for pair in Uri().pairs(value):
                pair.line = lineno
                yield pair
