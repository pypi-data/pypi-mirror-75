"""
Script to make sure the repo is good enough for running tests, meets SDLC, etc.

Basically, antyhing you want to put here that will be part of your automated
PR checking and whatever santiy checking you want for the CICD server to be confident
that it can start a test run without any missing packages, syntax errors, etc.

We're leaning in to using 'pre-commit' but this script can still be used
to run or check things that aren't a good fit for 'pre-commit'.

Runs the following commands:
    {}
"""
import argparse

from .utils import execute_command_list, CONFIGS
from .env_setup import env_setup
from .check_version import check_version


__commands_to_run = CONFIGS["self_check_commands"]

__doc__ = __doc__.format("\n    ".join(__commands_to_run))


def self_check(do_setup=False, do_version_check=False, verbose=True):
    """Run code checks."""
    if do_setup:
        env_setup(verbose)

    execute_command_list(__commands_to_run, verbose=verbose)

    if do_version_check:
        check_version()


def main():
    """Self check with cli args."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=__doc__
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help='run "env-setup" before running self checks',
    )
    parser.add_argument(
        "--check-version",
        action="store_true",
        help='run "check-version" after running self-checks',
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="do not show each command before it is executed",
    )
    args = parser.parse_args()

    self_check(
        do_setup=args.setup, do_version_check=args.check_version, verbose=not args.quiet
    )
