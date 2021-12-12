import logging
from argparse import ArgumentParser, Namespace
from functools import wraps
from sys import argv, stdout

from whispers.__version__ import __version__, __whispers__
from whispers.core.utils import DEFAULT_PATH, default_rules


def argument_parser() -> ArgumentParser:
    """CLI argument parser"""
    args_parser = ArgumentParser("whispers", description=("Identify secrets in static structured text."))
    args_parser.add_argument("-i", "--info", action="store_true", help="show extended help and exit")
    args_parser.add_argument("-c", "--config", help="config file")
    args_parser.add_argument(
        "-C", "--print_config", default=False, action="store_true", help="print default config and exit"
    )
    args_parser.add_argument("-o", "--output", help="output file")
    args_parser.add_argument("-e", "--exitcode", default=0, type=int, help="exit code on success")
    args_parser.add_argument("-r", "--rules", help="csv of rule IDs to report (see --info)")
    args_parser.add_argument("-R", "--xrules", help="csv of rule IDs to exclude (see --info)")
    args_parser.add_argument("-g", "--groups", help="csv of rule groups to report (see --info)")
    args_parser.add_argument("-G", "--xgroups", help="csv of rule groups to exclude (see --info)")
    args_parser.add_argument("-s", "--severity", help="csv of severity levels to report (see --info)")
    args_parser.add_argument("-S", "--xseverity", help="csv of severity levels to exclude (see --info)")
    args_parser.add_argument("-l", "--log", default=False, action="store_true", help="write /tmp/whispers.log")
    args_parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        const=logging.DEBUG,
        default=logging.INFO,
        help="log debugging information",
    )
    args_parser.add_argument("-v", "--version", action="version", version=__version__)
    args_parser.add_argument("src", nargs="?", help="target file or directory")

    args_parser.print_help = show_splash(args_parser.print_help)

    return args_parser


def parse_args(arguments: list = argv[1:]) -> Namespace:
    """Parses a list into a namespace"""
    args, _ = argument_parser().parse_known_args(arguments)

    if args.info:
        show_info()
        exit()

    if args.print_config:
        show_config()
        exit()

    if not args.src:
        argument_parser().print_help()
        exit()

    if args.output:
        args.output = open(args.output, "w")
    else:
        args.output = stdout

    if args.rules:
        args.rules = args.rules.split(",")

    if args.xrules:
        args.xrules = args.xrules.split(",")

    if args.groups:
        args.groups = args.groups.split(",")

    if args.xgroups:
        args.xgroups = args.xgroups.split(",")

    if args.severity:
        args.severity = args.severity.split(",")

    if args.xseverity:
        args.xseverity = args.xseverity.split(",")

    args.log |= args.debug == logging.DEBUG

    return args


def show_splash(func, **kwargs):
    @wraps(func)
    def splash(*args, **kwargs):
        print(__whispers__)
        print(__version__.rjust(64), end="\n\n")
        return func(*args, **kwargs)

    return splash


def show_config():
    print(DEFAULT_PATH.joinpath("config.yml").read_text())


def show_info():
    argument_parser().print_help()
    rules_table = []
    col_width = 20
    for rule in default_rules():
        line = (
            "    "
            + rule["group"].ljust(col_width)[:col_width]
            + " | "
            + rule["id"].ljust(col_width)[:col_width]
            + " | "
            + rule["severity"].ljust(col_width)[:col_width]
        )
        rules_table.append(line)

    draw_line = "\n  " + ("+--" + "-" * col_width) * 3 + "+"
    print(
        "\n\nrules:\n"
        + draw_line
        + "\n  | "
        + "group".ljust(col_width)
        + " | "
        + "rule id".ljust(col_width)
        + " | "
        + "severity".ljust(col_width)
        + " |"
        + draw_line
        + "\n"
        + "\n".join(sorted(rules_table))
        + draw_line
        + "\n\nreadme:  https://github.com/adeptex/whispers\n"
    )
