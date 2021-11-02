from dataclasses import InitVar, dataclass, field
from re import compile
from typing import Dict, List, Optional

from whispers.core.utils import DEFAULT_SEVERITY, default_rules, list_rule_ids


@dataclass
class Include:
    """AppConfig include configuration class"""

    files: List = field(default_factory=lambda: ["**/*"])  # globs


@dataclass
class Exclude:
    """AppConfig exclude configuration class"""

    files: Optional[List] = None  # regex
    keys: Optional[List] = None  # regex
    values: Optional[List] = None  # regex

    def __post_init__(self) -> None:
        """
        Create a single regex statement from each list,
        and compile it for efficient matching.
        """
        for key, value in self.__dict__.items():
            if not value:
                continue

            unified = "|".join(value)
            self.__dict__[key] = compile(unified)


@dataclass
class AppConfig:
    """Main application configuration class"""

    _config: InitVar[Dict]
    include: Include = field(default_factory=Include)
    exclude: Exclude = field(default_factory=Exclude)
    rules: List = field(default_factory=list)
    severity: List = field(default_factory=list)

    def __init__(self, config: Dict) -> None:
        self.include = Include(**config.get("include", {}))
        self.exclude = Exclude(**config.get("exclude", {}))
        self.rules = config.get("rules", list_rule_ids(default_rules()))
        self.severity = config.get("severity", DEFAULT_SEVERITY)
