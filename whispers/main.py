import json
import logging
from argparse import Namespace
from itertools import chain
from os import environ
from sys import exit
from typing import Iterator

from whispers.core.args import parse_args
from whispers.core.config import load_config
from whispers.core.pairs import make_pairs
from whispers.core.rules import load_rules
from whispers.core.scope import load_scope
from whispers.core.secrets import detect_secrets
from whispers.models.pair import KeyValuePair

environ["PYTHONUTF8"] = "1"
environ["PYTHONIOENCODING"] = "UTF-8"


def main() -> None:  # pragma: no cover
    """Main entry point"""
    args = parse_args()

    secrets = []
    for secret in run(args):
        logging.warning(str(secret))
        secrets.append(secret.to_json())

    args.output.write(json.dumps(secrets) + "\n")

    exit(args.exitcode)


def run(args: Namespace) -> Iterator[KeyValuePair]:
    """Main worker process"""
    config = load_config(args)
    rules = load_rules(args, config)
    scope = load_scope(args, config)
    parsed = map(lambda file: make_pairs(config, file), scope)
    detected = map(lambda pairs: detect_secrets(rules, pairs), parsed)
    secrets = chain.from_iterable(detected)

    return secrets


if __name__ == "__main__":
    main()
