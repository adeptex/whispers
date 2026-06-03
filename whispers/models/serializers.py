"""
JSON serializers for Rule and Specification models.

Usage::

    from whispers.models.rule import Rule
    from whispers.models.serializers import RuleSerializer, SpecificationSerializer

    # Build a Rule from a config dict (the normal whispers workflow)
    rule = Rule({
        "id": "secret-token",
        "group": "keys",
        "message": "Hard-coded secret token",
        "severity": "CRITICAL",
        "key": {"regex": "token|secret", "ignorecase": True, "minlen": 4},
        "value": {"regex": ".+", "minlen": 8, "isBase64": False},
        "similar": 0.8,
    })

    # Serialize to a Python dict
    rule_dict = RuleSerializer.to_dict(rule)

    # Serialize directly to a JSON string (kwargs forwarded to json.dumps)
    rule_json = RuleSerializer.to_json(rule, indent=2)

    # Serialize just a Specification
    spec_json = SpecificationSerializer.to_json(rule.key, indent=2)

    # Round-trip: reconstruct the Rule from the serialized dict
    restored = Rule(rule_dict)
"""

import json
import re
from typing import Any, Dict, Optional

from whispers.models.rule import Rule, Specification


class SpecificationSerializer:
    """JSON serializer for the Specification dataclass."""

    @staticmethod
    def to_dict(spec: Optional[Specification]) -> Optional[Dict[str, Any]]:
        if spec is None:
            return None

        result = {}

        if spec.regex is not None:
            result["regex"] = spec.regex.pattern
            result["ignorecase"] = bool(spec.regex.flags & re.IGNORECASE)
        else:
            result["ignorecase"] = spec.ignorecase

        if spec.minlen:
            result["minlen"] = spec.minlen
        if spec.isBase64 is not None:
            result["isBase64"] = spec.isBase64
        if spec.isAscii is not None:
            result["isAscii"] = spec.isAscii
        if spec.isUri is not None:
            result["isUri"] = spec.isUri
        if spec.isLuhn is not None:
            result["isLuhn"] = spec.isLuhn
        if spec.isFile:
            result["isFile"] = spec.isFile

        return result

    @staticmethod
    def to_json(spec: Optional[Specification], **kwargs) -> str:
        return json.dumps(SpecificationSerializer.to_dict(spec), **kwargs)


class RuleSerializer:
    """JSON serializer for the Rule dataclass."""

    @staticmethod
    def to_dict(rule: Rule) -> Dict[str, Any]:
        result = {
            "id": rule.id,
            "group": rule.group,
            "message": rule.message,
            "severity": rule.severity,
        }

        key_dict = SpecificationSerializer.to_dict(rule.key)
        if key_dict is not None:
            result["key"] = key_dict

        value_dict = SpecificationSerializer.to_dict(rule.value)
        if value_dict is not None:
            result["value"] = value_dict

        if rule.similar != 1:
            result["similar"] = rule.similar

        return result

    @staticmethod
    def to_json(rule: Rule, **kwargs) -> str:
        return json.dumps(RuleSerializer.to_dict(rule), **kwargs)


if __name__ == "__main__":
    rule = Rule(
        {
            "id": "secret-token",
            "group": "keys",
            "message": "Hard-coded secret token",
            "severity": "CRITICAL",
            "key": {"regex": "token|secret", "ignorecase": True, "minlen": 4},
            "value": {"regex": ".+", "minlen": 8, "isBase64": False},
            "similar": 0.8,
        }
    )

    print("=== Rule JSON ===")
    print(RuleSerializer.to_json(rule, indent=2))

    print("\n=== Key Specification JSON ===")
    print(SpecificationSerializer.to_json(rule.key, indent=2))

    print("\n=== Round-trip check ===")
    restored = Rule(RuleSerializer.to_dict(rule))
    print(f"Original id: {rule.id}, Restored id: {restored.id}")
    print(f"Match: {RuleSerializer.to_dict(rule) == RuleSerializer.to_dict(restored)}")
