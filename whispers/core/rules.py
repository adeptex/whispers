import logging
from argparse import Namespace
from typing import List

from whispers.core.utils import default_rules
from whispers.models.appconfig import AppConfig
from whispers.models.rule import Rule


def load_rules(args: Namespace, config: AppConfig) -> List[dict]:
    """Loads applicable rules based on args and config"""
    applicable_rules = []

    # Load from default rules based on rules/severity config
    for rule in default_rules():
        rule_id = rule.get("id", None)
        rule_group = rule.get("group", None)
        rule_severity = rule.get("severity", None)

        if rule_id in config.exclude.rules:
            continue  # Rule excluded

        if rule_id not in config.include.rules:
            continue  # Rule not included

        if rule_group in config.exclude.groups:
            continue  # Group excluded

        if rule_group not in config.include.groups:
            continue  # Group not included

        if rule_severity in config.exclude.severity:
            continue  # Severity excluded

        if rule_severity not in config.include.severity:
            continue  # Severity not included

        applicable_rules.append(Rule(rule))

    # Load inline rules from config file (if any)
    for rule in config.include.rules:
        if isinstance(rule, str):
            continue  # Not an inline rule

        applicable_rules.append(Rule(rule))

    logging.debug(f"load_rules loaded {len(applicable_rules)} rules")
    return applicable_rules
