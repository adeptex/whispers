import re
from pathlib import Path
from typing import Iterator

import yaml
from yaml.parser import ParserError
from yaml.resolver import Resolver

from whispers.core.utils import global_exception_handler
from whispers.models.pair import KeyValuePair
from whispers.plugins.traverse import StructuredDocument


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

            # Quote unquoted mustache placeholders such as {{ value }}. A plain
            # containment check replaces the previous `.+(\[)?\{\{.*\}\}(\])?`
            # regex, which backtracked quadratically on long lines carrying many
            # `{{` with no matching `}}` (hanging for minutes/hours on some files).
            if "{{" in line and "}}" in line:
                line = line.replace("{{", "'{{").replace("}}", "}}'")

            document += line

        document = self._strip_template_blocks(document)
        document = re.sub(r"^#.*$", "", document)

        # Load converted YAML
        try:
            yaml.add_multi_constructor("", _constructor, Loader=yaml.SafeLoader)
            code = yaml.safe_load(document)
            yield from self.traverse(code)

        except ParserError:
            global_exception_handler(filepath.as_posix(), document)

    @staticmethod
    def _strip_template_blocks(document: str) -> str:
        """Remove {%...%} and <%...%> template blocks in a single linear pass.

        Behaviour-equivalent to re.sub(r"[<{]%.*?%[}>]", "", document, DOTALL):
        each opener ({% or <%) is removed up to its nearest closing %} or %>.
        The regex form backtracks quadratically on documents with many unbalanced
        template markers (e.g. Jekyll/Liquid pages), which could hang whispers for
        hours; this scan is linear.
        """
        out = []
        i = 0
        n = len(document)

        while i < n:
            char = document[i]

            if char in "<{" and i + 1 < n and document[i + 1] == "%":
                cursor = i + 2
                close = -1

                while True:
                    percent = document.find("%", cursor)
                    if percent == -1:
                        break
                    if percent + 1 < n and document[percent + 1] in "}>":
                        close = percent
                        break
                    cursor = percent + 1

                if close == -1:
                    # No closing marker remains anywhere: nothing left to strip.
                    out.append(document[i:])
                    break

                i = close + 2
                continue

            out.append(char)
            i += 1

        return "".join(out)
