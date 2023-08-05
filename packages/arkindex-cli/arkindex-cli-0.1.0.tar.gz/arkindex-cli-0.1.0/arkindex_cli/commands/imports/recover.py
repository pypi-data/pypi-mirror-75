# -*- coding: utf-8 -*-
from typing import Optional
from urllib.parse import urljoin
from uuid import UUID

from rich import print
from rich.progress import Progress

from arkindex_cli.auth import Profiles
from arkindex_cli.commands.imports.base import get_global_report, get_import
from arkindex_cli.utils import ask


def add_recover_parser(subcommands) -> None:
    recover_parser = subcommands.add_parser(
        "recover",
        description="Start a new DataImport from the failed elements of another",
        help="Start a new DataImport from the failed elements of another",
    )
    recover_parser.add_argument(
        "import_id",
        type=UUID,
        help="ID of the DataImport to retrieve the elements from",
    )
    recover_parser.add_argument(
        "-r",
        "--run",
        dest="run_number",
        type=int,
        help="Workflow run number to retrieve a report for. Defaults to the latest run.",
    )
    recover_parser.set_defaults(func=run)


def run(import_id: UUID, run_number: Optional[int] = None) -> int:
    with Progress(transient=True) as progress:
        progress.add_task(start=False, description="Loading API client")
        # TODO: Profile name argument
        profiles = Profiles()
        # The profile URL is used later on
        profile = profiles.get_default_profile()
        client = profiles.get_default_client()

    if not client:
        print(
            "[bright_red]No default profile found. Try logging in using [white]arkindex login[/] first."
        )
        return

    try:
        ml_report = get_global_report(client, import_id, run_number)
    except ValueError as e:
        print(f"[bright_red]{e}")
        return 2

    failed_elements = list(ml_report.failed_elements.keys())
    if not failed_elements:
        print(
            "[bright_yellow]There are no failed elements to retry on this DataImport."
        )
        return 2

    selected_count = len(client.paginate("ListSelection"))
    if selected_count:
        print(
            f"{selected_count} elements are currently selected. This script will clear the selection before selecting failed elements."
        )
        if ask("Clear and continue?", default="yes") != "yes":
            print("Aborting.")
            return 2

        with Progress(transient=True) as progress:
            progress.add_task(start=False, description="Clearing selection")
            client.request("RemoveSelection", body={})

    with Progress(transient=True) as progress:
        progress.add_task(
            start=False, description=f"Selecting {len(failed_elements)} failed elements"
        )
        client.request("AddSelection", body={"ids": failed_elements})

    # TODO: Create a DataImport with Workers mode and give a link to the worker configuration page
    corpus_id = get_import(client, import_id)["corpus"]
    config_url = urljoin(profile.url, f"imports/corpus/{corpus_id}?selection=true")

    print(f"{len(failed_elements)} elements selected.")
    print(
        f"You may now configure and start a new workflow using the Arkindex frontend: [bright_blue underline]{config_url}"
    )
