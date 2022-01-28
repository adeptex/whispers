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
    rule: Dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.keypath == []:
            self.keypath = [self.key]

    def __repr__(self) -> str:
        return f"{self.key} = {self.value}"
