# -*- coding: utf-8 -*-
import logging

from rich import traceback
from rich.logging import RichHandler

# Colorful logging
# https://rich.readthedocs.io/en/latest/logging.html
logging.basicConfig(
    level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)

# Add colorful tracebacks to crash with elegance
# https://rich.readthedocs.io/en/latest/traceback.html
traceback.install()
