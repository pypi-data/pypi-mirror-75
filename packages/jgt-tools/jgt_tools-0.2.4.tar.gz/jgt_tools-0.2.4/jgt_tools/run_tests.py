"""
Run all available tests.

Runs the following commands:
    {}
"""
import argparse

from .utils import execute_command_list, CONFIGS
from .env_setup import env_setup
from .self_check import self_check as run_self_check

__commands_to_run = CONFIGS["run_tests_commands"]


__doc__ = __doc__.format("\n    ".join(__commands_to_run))


def run_tests(do_setup=False, self_check=False, verbose=True):
    """Run code checks."""
    if do_setup:
        env_setup(verbose)
    if self_check:
        run_self_check(verbose=verbose)

    execute_command_list(__commands_to_run, verbose=verbose)


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
        "--check", action="store_true", help='run "self-check" before running tests'
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="do not show each command before it is executed",
    )
    args = parser.parse_args()

    run_tests(do_setup=args.setup, self_check=args.check, verbose=not args.quiet)
