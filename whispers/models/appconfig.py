import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Pattern

from whispers.core.constants import DEFAULT_SEVERITY
from whispers.core.utils import default_rules, list_rule_prop, load_regex

DEFAULT_RULES = default_rules()


@dataclass
class Include:
    """AppConfig include configuration class"""

    files: Optional[List] = field(default_factory=lambda: ["**/*"])  # globs
    rules: Optional[List] = field(default_factory=lambda: list_rule_prop("id", DEFAULT_RULES))
    groups: Optional[List] = field(default_factory=lambda: list_rule_prop("group", DEFAULT_RULES))
    severity: Optional[List] = field(default_factory=lambda: DEFAULT_SEVERITY)


@dataclass
class Exclude:
    """AppConfig exclude configuration class"""

    files: Optional[Pattern] = field(default_factory=lambda: None)  # regex
    keys: Optional[Pattern] = field(default_factory=lambda: None)  # regex
    values: Optional[Pattern] = field(default_factory=lambda: None)  # regex
    rules: Optional[List] = field(default_factory=list)
    groups: Optional[List] = field(default_factory=list)
    severity: Optional[List] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.files = self._compile("files")
        self.keys = self._compile("keys")
        self.values = self._compile("values")

    def _compile(self, idx) -> Optional[Pattern]:
        """
        Create a single regex statement from a list,
        and compile it for efficient matching.
        """
        regex_list = self.__dict__[idx]
        if regex_list is None:
            return None

        return load_regex("|".join(regex_list), flags=re.IGNORECASE)


@dataclass
class AppConfig:
    """Main application configuration class"""

    include: Include = field(default_factory=Include)
    exclude: Exclude = field(default_factory=Exclude)
    ast: bool = True

    def __init__(self, config: Dict = {}) -> None:
        self.include = Include(**config.get("include", {}))
        self.exclude = Exclude(**config.get("exclude", {}))
        self.ast = config.get("ast", False)
