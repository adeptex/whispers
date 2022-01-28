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

    def common_pairs(self, text: str, lineno: int) -> Iterator[KeyValuePair]:
        yield from Common(line=lineno).pairs(text)
        yield from self.parse_pk(text)

    @staticmethod
    def parse_pk(text: str) -> Iterator[KeyValuePair]:
        """Check if text resembles a Private Key (PK), only for plaintext files"""
        if not (text.startswith("-----") and text.endswith("-----")):
            return []

        if len(text) < 15:
            return []

        yield KeyValuePair("private_key", text)
