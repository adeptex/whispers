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
        regex_unquoted = re.compile(r".+(\[)?\{\{.*\}\}(\])?")
        document = ""

        for line in filepath.open("r").readlines():
            if line.startswith("---"):
                continue

            if regex_unquoted.match(line):
                line = line.replace("{{", "'{{").replace("}}", "}}'")

            document += line

        document = re.sub(r"[<{]%.*?%[}>]", "", document, flags=re.MULTILINE | re.DOTALL)
        document = re.sub(r"^#.*$", "", document)

        # Load converted YAML
        try:
            yaml.add_multi_constructor("", _constructor, Loader=yaml.SafeLoader)
            code = yaml.safe_load(document)
            yield from self.traverse(code)

        except ParserError:
            global_exception_handler(filepath.as_posix(), document)
