import json
import re
from pathlib import Path
from typing import Dict, Iterator

from whispers.core.utils import global_exception_handler
from whispers.models.pair import KeyValuePair
from whispers.plugins.traverse import StructuredDocument


class Json(StructuredDocument):
    def pairs(self, filepath: Path) -> Iterator[KeyValuePair]:
        """
        Try to load as as. Otherwise, try to
        """
        try:
            document = json.load(filepath.open())

        except json.decoder.JSONDecodeError:
            document = self.load_custom_json(filepath)

        yield from self.traverse(document)

    @staticmethod
    def load_custom_json(filepath: Path) -> Dict:
        """
        Try converting custom JSON to a parsable format:
        - Remove lines that start with // comments
        - Strip // comments from the end the line
        """
        document = ""
        for line in filepath.open("r").readlines():
            if line.startswith("//"):
                continue
            line = re.sub(r" // ?.*$", "", line)
            document += line

        try:
            return json.loads(document)

        except Exception:
            global_exception_handler(filepath.as_posix(), document)
            return {}
