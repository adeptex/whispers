import shlex
from pathlib import Path
from typing import Iterator, List, Tuple

from whispers.core.utils import ESCAPED_CHARS, KeyValuePair, global_exception_handler, strip_string


class Shell:
    def pairs(self, filepath: Path) -> Iterator[KeyValuePair]:
        for cmdline, lineno in self.read_commands(filepath):
            try:
                cmd = shlex.split(cmdline)
            except Exception:
                global_exception_handler(filepath.as_posix(), cmdline)
                continue

            if not cmd:
                continue

            yield from self.variables(cmd, lineno)

            if cmd[0].lower() == "curl":
                yield from self.curl(cmd, lineno)

    def read_commands(self, filepath: Path) -> Tuple[str, int]:
        ret = []
        for lineno, line in enumerate(filepath.open(), 1):
            line = line.strip()
            if line.startswith("#"):  # Comments
                line = line.lstrip("#").strip()
                line = line.translate(ESCAPED_CHARS)

            elif line.endswith("\\"):  # Multi-line commands
                ret.append(line[:-1])
                continue

            ret.append(line)
            yield " ".join(ret), lineno
            ret = []

    def variables(self, cmd: List[str], lineno: int = 0) -> Iterator[KeyValuePair]:
        """
        Checks if Shell variables contain a hardcoded or a default value.
        Examples:
            password="defaultPassword"
            password=${ENV_VAR:-defaultPassword}
        """
        for value in cmd:
            key = ""

            if "=" in value and len(value.split("=")) == 2:
                key, value = value.split("=")  # Variable assignment

            if ":-" in value and value.startswith("${") and value.endswith("}"):
                key, value = value[2:-1].split(":-")  # Default value

            if not (key or value):
                continue

            yield KeyValuePair(key, value, line=lineno)

    def curl(self, cmd: List[str], lineno: int) -> Iterator[KeyValuePair]:
        key = "password"
        indicators_combined = ["-u", "--user", "-U", "--proxy-user", "-E", "--cert"]
        indicators_single = ["--tlspassword", "--proxy-tlspassword"]
        indicators = indicators_combined + indicators_single
        for indicator in indicators:
            if indicator not in cmd:
                continue

            idx = cmd.index(indicator)
            if len(cmd) == idx + 1:
                continue  # End of command

            credentials = strip_string(cmd[idx + 1])
            if indicator in indicators_single:
                yield KeyValuePair(key, credentials, [key])

            else:
                if ":" not in credentials:
                    continue  # Password not specified

                yield KeyValuePair(key, credentials.split(":")[1], keypath=[key], line=lineno)
