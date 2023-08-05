"""Shared util functions."""
from collections import defaultdict
import csv
from pathlib import Path
import shlex
import subprocess
import sys

import tomlkit


DEFAULTS_FILE = Path(__file__).parent / "data" / "defaults.csv"


def execute_command_list(commands_to_run, verbose=True):
    """
    Execute each command in the list.

    If any command fails, print a helpful message and exit with that status.
    """
    for command in commands_to_run:
        if verbose:
            print(f"+{command}")
        job = subprocess.run(shlex.split(command))
        if job.returncode:
            sys.exit(job.returncode)


_DEFAULT_CONFIGS: defaultdict = defaultdict(list)


def _load_defaults():
    with DEFAULTS_FILE.open() as f:
        for group, cmd in csv.reader(f):
            _DEFAULT_CONFIGS[group].append(cmd)


_load_defaults()


def _get_package_root():
    try:
        return Path(
            subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"], universal_newlines=True
            ).split("\n")[0]
        )
    except subprocess.CalledProcessError:
        print("jgt_tools needs to be run from within a git repository")
        sys.exit(1)


PACKAGE_ROOT_PATH = _get_package_root()


def get_pyproject_config():
    """Get the config data from the project's pyproject.toml file."""
    pyproject_path = PACKAGE_ROOT_PATH / "pyproject.toml"
    if not pyproject_path.exists():
        raise FileNotFoundError(
            f"Config file not found at: '{pyproject_path}' "
            "(must be run from project root)"
        )
    with pyproject_path.open() as f:
        pyproject = tomlkit.loads(f.read())
    return pyproject


def load_configs():
    """Build configs from defaults and pyproject.toml."""
    pyproject = get_pyproject_config()

    poetry = pyproject["tool"]["poetry"]
    package_name = poetry["name"]
    package_description = poetry["description"]

    configs = {
        **_DEFAULT_CONFIGS,
        "package_name": package_name,
        "description": package_description,
        "base_dir": PACKAGE_ROOT_PATH,
    }
    if "jgt_tools" in pyproject["tool"]:
        configs = {**configs, **pyproject["tool"]["jgt_tools"]}
    return configs


CONFIGS = load_configs()


def owner_name_from(origin_url):
    """
    Extract the owner name from a git origin URL.

    The git origin URL might be in ``git+ssh`` form, or ``https`` form.

    Args:
        origin_url (str): Origin URL from `git`

    Returns:
        str: A slash-separated string containing the organization / owner and repository

    Examples:
        >>> owner_name_from("git@github.com:jolly-good-toolbelt/jgt_tools.git")
        "jolly-good-toolbelt/jgt_tools"
        >>> owner_name_from("https://github.com/jolly-good-toolbelt/jgt_tools.git")
        "jolly-good-toolbelt/jgt_tools"

    """
    if not origin_url:
        return ""
    owner_name = origin_url.split(":")[1]  # Remove method portion
    owner_name = owner_name.rsplit(".", 1)[0]  # Remove `.git`
    # Keep only the last two parts that remain, which are the org/owner and repo name
    return "/".join(owner_name.split("/")[-2:])
