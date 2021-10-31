import logging
from base64 import b64decode
from typing import Iterable, Iterator, Optional

from whispers.core.utils import (
    KeyValuePair,
    find_line_number,
    is_ascii,
    is_base64,
    is_base64_bytes,
    is_luhn,
    is_similar,
    is_uri,
)


def detect_secrets(rules: list, pairs: Iterable[KeyValuePair]) -> Iterator[KeyValuePair]:
    """Detect pairs with hardcoded secrets"""
    for pair in pairs:
        detected = filter(None, map(lambda rule: filter_rule(rule, pair), rules))
        tagged = map(tag_lineno, detected)

        yield from tagged


def tag_lineno(pair: KeyValuePair) -> KeyValuePair:
    """Add pair line number"""
    pair.line = find_line_number(pair)
    return pair


def filter_rule(rule: dict, pair: KeyValuePair) -> Optional[KeyValuePair]:
    """Filters based on rule"""
    if not filter_param("key", rule, pair):
        logging.debug(f"filter_rule '{rule['id']}' excluded key '{pair.key}'")
        return None

    if not filter_param("value", rule, pair):
        logging.debug(f"filter_rule '{rule['id']}' excluded value '{pair.value}'")
        return None

    if is_similar(pair.key, pair.value, rule["similar"]):
        logging.debug(f"filter_rule '{rule['id']}' excluded similar '{pair.key}'/'{pair.value}'")
        return None

    pair.rule = {
        "id": rule["id"],
        "severity": rule["severity"],
        "message": rule["message"],
    }

    logging.debug(f"filter_rule included pair '{pair}'")
    return pair


def filter_param(idx: str, rule: dict, pair: KeyValuePair) -> Optional[KeyValuePair]:
    """Filters based on key/value rule definition"""
    if idx not in rule:
        return pair

    isBase64 = rule[idx].get("isBase64", False)
    isAscii = rule[idx].get("isAscii", True)
    isUri = rule[idx].get("isUri", False)
    isLuhn = rule[idx].get("isLuhn", False)
    minlen = rule[idx].get("minlen", 0)
    regex = rule[idx].get("regex", None)

    target = pair.__dict__[idx]

    if isBase64:
        if is_base64(target) and isAscii:
            target = b64decode(target).decode("utf-8")
        elif is_base64_bytes(target) and not isAscii:
            target = b64decode(target)
        else:
            logging.debug(f"filter_param isBase64={isBase64} excluded '{target}'")
            return None

    if isAscii != is_ascii(target):
        logging.debug(f"filter_param isAscii={isAscii} excluded '{target}'")
        return None

    if isUri != is_uri(target):
        logging.debug(f"filter_param isUri={isUri} excluded '{target}'")
        return None

    if isLuhn != is_luhn(target):
        logging.debug(f"filter_param isLuhn={isLuhn} excluded '{target}'")
        return None

    target = pair.__dict__[idx]

    if minlen > len(target):
        logging.debug(f"filter_param minlen={minlen} excluded '{target}'")
        return None

    if regex and not regex.match(target):
        logging.debug(f"filter_param regex={regex} excluded '{target}'")
        return None

    logging.debug(f"filter_param included '{pair}'")
    return pair
