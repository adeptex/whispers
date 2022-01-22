import json
from argparse import Namespace
from sys import stdout

from whispers.models.pair import KeyValuePair


def printer(args: Namespace, pair: KeyValuePair) -> str:
    """Prints formatted pair data to given output"""
    if args.output is stdout:
        fmt = (
            f"[{pair.file}:{pair.line}:{pair.rule.group}:{pair.rule.id}:{pair.rule.severity}]"
            + f" {pair.key} = {pair.value}"
        )

    else:
        fmt = json.dumps(
            {
                "key": pair.key,
                "value": pair.value,
                "file": pair.file,
                "line": pair.line,
                "rule_id": pair.rule.id,
                "message": pair.rule.message,
                "severity": pair.rule.severity,
            }
        )

    print(fmt, file=args.output)
    return fmt
