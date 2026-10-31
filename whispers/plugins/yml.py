import re
from pathlib import Path
from typing import Iterator

import yaml
from yaml.parser import ParserError
from yaml.scanner import ScannerError
from yaml.resolver import Resolver

from whispers.core.utils import global_exception_handler
from whispers.models.pair import KeyValuePair
from whispers.plugins.traverse import StructuredDocument


def _has_unquoted_template(line: str) -> bool:
    r"""Linear replacement for the `.+(\[)?\{\{.*\}\}(\])?` match.

    The regex only asks: is there a `{{` with at least one character
    before it, followed somewhere later by `}}`? Checking the first
    such `{{` is enough: any `}}` after a later `{{` is also after
    the first one. Two str.find calls, no backtracking.
    """
    start = line.find("{{", 1)
    return start != -1 and line.find("}}", start + 2) != -1


def _strip_template_tags(document: str) -> str:
    r"""Linear replacement for re.sub(r"[<{]%.*?%[}>]", "", document, DOTALL).

    Single left-to-right pass: each opener is removed up to its
    nearest closer (`%}` or `%>`), exactly like the lazy `.*?`
    semantics. An opener with no closer anywhere after it is left in
    place. The cursor only moves forward, so this is linear in the
    document length instead of quadratic (ReDoS, see issue #206).
    """
    parts = []
    pos = 0
    while True:
        open_idx = -1
        for opener in ("{%", "<%"):
            idx = document.find(opener, pos)
            if idx != -1 and (open_idx == -1 or idx < open_idx):
                open_idx = idx
        if open_idx == -1:
            parts.append(document[pos:])
            break
        close_idx = -1
        for closer in ("%}", "%>"):
            idx = document.find(closer, open_idx + 2)
            if idx != -1 and (close_idx == -1 or idx < close_idx):
                close_idx = idx
        if close_idx == -1:
            parts.append(document[pos:])
            break
        parts.append(document[pos:open_idx])
        pos = close_idx + 2
    return "".join(parts)


class Yml(StructuredDocument):
    def __init__(self):
        super().__init__()

        # Remove resolvers for on/off/yes/no
        list(map(lambda idx: Resolver.yaml_implicit_resolvers.pop(idx, None), "OoYyNn"))

    def pairs(self, filepath: Path) -> Iterator[KeyValuePair]:
        def _constructor(loader, tag_suffix, node):
            """This is needed to parse IaC syntax"""
            ret = loader.construct_scalar(node)
            return f"{tag_suffix} {ret}"

        """
        Convert custom YAML to parsable YAML
        - Skip ---
        - Quote unquoted values such as {{ placeholder }}
        - Remove text between <% %> and {% %}
        - Remove comments that start with #
        """
        document = ""

        for line in filepath.open("r").readlines():
            if line.startswith("---"):
                continue

            if _has_unquoted_template(line):
                line = line.replace("{{", "'{{").replace("}}", "}}'")

            document += line

        document = _strip_template_tags(document)
        document = re.sub(r"^#.*$", "", document)

        # Load converted YAML
        try:
            yaml.add_multi_constructor("", _constructor, Loader=yaml.SafeLoader)
            code = yaml.safe_load(document)
            yield from self.traverse(code)

        except (ParserError, ScannerError):
            global_exception_handler(filepath.as_posix(), document)
