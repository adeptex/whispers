import logging
from argparse import Namespace
from typing import List

from whispers.core.utils import default_rules
from whispers.models.appconfig import AppConfig
from whispers.models.rule import Rule


def load_rules(args: Namespace, config: AppConfig) -> List[dict]:
    """Loads applicable rules based on args and config"""
    include_rule_ids = args.rules or config.include.rules
    exclude_rule_ids = args.xrules or config.exclude.rules
    include_groups = args.groups or config.include.groups
    exclude_groups = args.xgroups or config.exclude.groups
    include_severity = args.severity or config.include.severity
    exclude_severity = args.xseverity or config.exclude.severity
    applicable_rules = []

    # Load from default rules based on rules/severity config
    for rule in default_rules():
        rule_id = rule.get("id", None)
        rule_group = rule.get("group", None)
        rule_severity = rule.get("severity", None)

        if rule_id in exclude_rule_ids:
            continue  # Rule excluded

        if rule_id not in include_rule_ids:
            continue  # Rule not included

        if rule_group in exclude_groups:
            continue  # Group excluded

        if rule_group not in include_groups:
            continue  # Group not included

        if rule_severity in exclude_severity:
            continue  # Severity excluded

        if rule_severity not in include_severity:
            continue  # Severity not included

        applicable_rules.append(Rule(rule))

    # Load inline rules from config file (if any)
    for rule in include_rule_ids:
        if isinstance(rule, str):
            continue  # Not an inline rule

        applicable_rules.append(Rule(rule))

    logging.debug(f"load_rules loaded {len(applicable_rules)} rules")
    return applicable_rules
