import logging
from typing import Iterable, Iterator, List, Optional

from whispers.core.utils import find_line_number
from whispers.models.pair import KeyValuePair
from whispers.models.rule import Rule


def detect_secrets(rules: List[Rule], pairs: Iterable[KeyValuePair]) -> Iterator[KeyValuePair]:
    """Detect pairs with hardcoded secrets"""
    for pair in pairs:
        detected = filter(None, map(lambda rule: filter_rule(rule, pair), rules))

        yield from detected


def filter_rule(rule: Rule, pair: KeyValuePair) -> Optional[KeyValuePair]:
    """Filters based on rule"""
    if not rule.matches(pair):
        logging.debug(f"filter_rule '{rule.id}' excluded pair '{pair}'")
        return None

    pair.rule = rule
    pair.line = find_line_number(pair)

    logging.debug(f"filter_rule '{rule.id}' included pair '{pair}'")
    return pair
