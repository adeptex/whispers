import re
from base64 import b64decode
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Pattern

from whispers.core.utils import is_ascii, is_base64, is_base64_bytes, is_luhn, is_similar, is_uri
from whispers.models.pair import KeyValuePair


@dataclass
class Specification:
    """Rule key/value specification class"""

    regex: Optional[Pattern] = None
    ignorecase: Optional[bool] = False
    minlen: Optional[int] = 0
    isBase64: Optional[bool] = None
    isAscii: Optional[bool] = None
    isUri: Optional[bool] = None
    isLuhn: Optional[bool] = None

    def __post_init__(self) -> None:
        """Compile regex with explicit ignorecase"""
        if self.regex is None:
            return None

        flags = re.IGNORECASE if self.ignorecase else 0
        self.regex = re.compile(self.regex, flags=flags)

    def matches(self, target: str) -> bool:
        if len(target) < self.minlen:
            return False

        if self.regex and not self.regex.match(target):
            return False

        if self.isBase64 is True:
            if is_base64(target) and self.isAscii is not False:
                target = b64decode(target).decode("utf-8")
            elif is_base64_bytes(target) and self.isAscii is False:
                target = b64decode(target)
            else:
                return False

        if self.isAscii is not None and self.isAscii is not is_ascii(target):
            return False

        if self.isUri is not None and self.isUri is not is_uri(target):
            return False

        if self.isLuhn is not None and self.isLuhn is not is_luhn(target):
            return False

        return True


@dataclass
class Rule:
    """Main rule configuration class"""

    id: str = field(default_factory=str)
    message: str = field(default_factory=str)
    severity: str = field(default_factory=str)
    key: Specification = field(default=None)
    value: Specification = field(default=None)
    similar: float = field(default_factory=float)

    def __init__(self, rule: Dict) -> None:
        self.id = self._get_required("id", rule)
        self.message = self._get_required("message", rule)
        self.severity = self._get_required("severity", rule)
        self.key = self._get_spec("key", rule)
        self.value = self._get_spec("value", rule)
        self.similar = rule.get("similar", 1)

    @staticmethod
    def _get_required(idx: str, rule: Dict) -> Any:
        """Get a required rule value"""
        value = rule.get(idx, False)
        if not value:
            raise IndexError(f"Missing rule '{idx}' specification: '{rule}'")

        return value

    @staticmethod
    def _get_spec(idx: str, rule: Dict) -> Optional[Specification]:
        """Get an optional rule specification"""
        spec = rule.get(idx, False)
        if not spec:
            return None

        if isinstance(spec, dict):
            return Specification(**spec)

        raise ValueError(f"Invalid rule '{idx}' specification: '{rule}'")

    def matches(self, pair: KeyValuePair) -> bool:
        if self.key and not self.key.matches(pair.key):
            return False

        if self.value and not self.value.matches(pair.value):
            return False

        if is_similar(pair.key, pair.value, self.similar):
            return False

        return True
