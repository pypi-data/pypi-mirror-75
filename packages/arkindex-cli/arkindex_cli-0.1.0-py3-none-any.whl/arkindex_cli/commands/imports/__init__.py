# -*- coding: utf-8 -*-
from arkindex_cli.commands.imports.recover import add_recover_parser
from arkindex_cli.commands.imports.report import add_report_parser


def add_import_parser(subcommands) -> None:
    import_parser = subcommands.add_parser(
        "import",
        aliases=["imports"],
        description="Manage DataImports",
        help="Manage DataImports",
    )
    subparsers = import_parser.add_subparsers()
    add_report_parser(subparsers)
    add_recover_parser(subparsers)
    import_parser.set_defaults(
        func=lambda: import_parser.error("A subcommand is required.")
    )
