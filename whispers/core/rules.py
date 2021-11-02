import logging
from argparse import Namespace
from typing import List

from whispers.core.utils import default_rules
from whispers.models.appconfig import AppConfig
from whispers.models.rule import Rule


def load_rules(args: Namespace, config: AppConfig) -> List[dict]:
    """Loads applicable rules based on args and config"""
    rule_ids = args.rules or config.rules
    severities = args.severity or config.severity
    applicable_rules = []

    # Load from default rules based on rules/severity config
    for rule in default_rules():
        rule_id = rule["id"].strip()
        rule_severity = rule["severity"].strip()

        if rule_id not in rule_ids:
            continue

        if rule_severity not in severities:
            continue

        applicable_rules.append(Rule(rule))

    # Load inline rules from config file (if any)
    for rule in rule_ids:
        if isinstance(rule, str):
            continue

        applicable_rules.append(Rule(rule))

    logging.debug(f"load_rules loaded {len(applicable_rules)} rules")
    return applicable_rules
