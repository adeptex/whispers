from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class KeyValuePair:
    """Main key-value pair class"""

    key: str
    value: str
    keypath: List = field(default_factory=list)
    file: str = ""
    line: int = 0
    rule: object = None

    def __post_init__(self) -> None:
        if self.keypath == []:
            self.keypath = [self.key]

    def __repr__(self) -> str:
        return f"[{self.file}:{self.line}] {self.key} = {self.value}"

    def to_json(self) -> Dict:
        return {
            "key": self.key,
            "value": self.value,
            "file": self.file,
            "line": self.line,
            "rule_id": self.rule.id,
            "message": self.rule.message,
            "severity": self.rule.severity,
        }
