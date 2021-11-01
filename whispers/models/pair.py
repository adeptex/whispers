from dataclasses import dataclass, field


@dataclass
class KeyValuePair:
    key: str
    value: str
    keypath: list = field(default_factory=list)
    file: str = ""
    line: int = 0
    rule: dict = field(default_factory=dict)

    def __post_init__(self, **kwargs) -> None:
        if self.keypath == []:
            self.keypath = [self.key]
