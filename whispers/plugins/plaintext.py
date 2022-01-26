from itertools import chain
from pathlib import Path
from typing import Iterator

from whispers.core.utils import strip_string
from whispers.models.pair import KeyValuePair
from whispers.plugins.common import Common


class Plaintext:
    def pairs(self, filepath: Path) -> Iterator[KeyValuePair]:
        for lineno, line in enumerate(filepath.open(), 1):
            line = strip_string(line)
            if not line:
                continue

            yield from self.common_pairs(line, lineno)

    @staticmethod
    def common_pairs(line: str, lineno: int) -> Iterator[KeyValuePair]:
        pairs = [Common().pairs(line), Common().parse_pk(line)]
        for pair in chain.from_iterable(pairs):
            pair.line = lineno
            yield pair
