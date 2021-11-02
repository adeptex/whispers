from dataclasses import dataclass, field


@dataclass
class KeyValuePair:
    """Main key-value pair class"""

    key: str
    value: str
    keypath: list = field(default_factory=list)
    file: str = ""
    line: int = 0
    rule: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.keypath == []:
            self.keypath = [self.key]

    def __repr__(self) -> str:
        return f"{self.key} = {self.value}"
