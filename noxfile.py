"""Nox sessions."""
import os
import shlex
import shutil
import sys
from pathlib import Path
from textwrap import dedent

import nox


try:
    from nox_poetry import Session
    from nox_poetry import session
except ImportError:
    message = f"""\
    Nox failed to import the 'nox-poetry' package.

    Please install it using the following command:

    {sys.executable} -m pip install nox-poetry"""
    raise SystemExit(dedent(message)) from None


package = "real_state_scraper_engine"
python_versions = ["3.12", "3.11"]
nox.needs_version = ">= 2024.1"
nox.options.sessions = (
    "tests",
)

@session(python=python_versions)
def tests(session: Session) -> None:
    """Run the test suite."""
    session.install(".")
    session.install("coverage[toml]", "pytest", "pygments")
    session.run("coverage", "run", "--parallel-mode", "--module", "pytest", *session.posargs)


