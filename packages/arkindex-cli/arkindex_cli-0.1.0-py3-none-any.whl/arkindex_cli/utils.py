# -*- coding: utf-8 -*-
from getpass import getpass

from rich import print


def ask(prompt: str, default: str = None, hidden: bool = False) -> str:
    """
    Ask for input with an optional default value.
    """
    if default is not None:
        # Add the default to the prompt
        # white is actually gray in a terminal, bright_white is white
        prompt += f" [/]({default})"

    print(f"[bold]{prompt}: ", end="")

    input_function = getpass if hidden else input
    return input_function("") or default
