# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jgt_tools', 'jgt_tools.docs']

package_data = \
{'': ['*'], 'jgt_tools': ['data/*']}

install_requires = \
['tomlkit>=0.5.3,<0.6.0']

extras_require = \
{'build_docs': ['sphinx>=2.1,<3.0',
                'sphinx-rtd-theme>=0.4.3,<0.5.0',
                'ghp-import>=0.5.5,<0.6.0']}

entry_points = \
{'console_scripts': ['build-and-push-docs = '
                     'jgt_tools.docs.build_docs:build_and_push[build_docs]',
                     'build-docs = jgt_tools.docs.build_docs:build[build_docs]',
                     'check-version = jgt_tools.check_version:check_version',
                     'env-setup = jgt_tools.env_setup:main',
                     'run-tests = jgt_tools.run_tests:main',
                     'self-check = jgt_tools.self_check:main']}

setup_kwargs = {
    'name': 'jgt-tools',
    'version': '0.2.4',
    'description': 'A collection of tools for commmon package scripts',
    'long_description': 'JGT Tools\n=========\n\nJGT Tools is a collection of package helpers\nfor common CLI functions\nwithin a properly-formatted repository.\n\n\nQuickstart\n----------\n\nJust include ``jgt_tools`` in your package VirtualEnv,\nand you\'ll have access to these CLI calls:\n\n- ``env-setup`` - set up the development environment\n  with all packages and pre-commit checks\n- ``self-check`` - run self-checks/linters/etc. on your repository\n- ``run-tests`` - run your in-repo test suite\n- ``build-docs`` - build repo documentation locally\n- ``build-and-push-docs`` - both build the docs,\n  then publish to your gh-pages branch\n- ``check-version`` - raise an error if package-relevant files have changed\n  without a version bump\n\nDetails for each script can be found by calling with the ``--help`` flag.\n\n\nDocumentation Index\n-------------------\n\nIn order to get the full benefit from ``build-docs``,\nit is encouraged to create an index file\nthat pulls together all the documentation.\nThis file needs to be in the root folder\nand should be called ``.jgt_tools.index``.\nThis will be moved into the working directory for Sphinx\nand be used when building the documentation.\nAdditional information can be found on the `Sphinx site`_.\n\nConfiguration\n-------------\n\nA number of the actions to be called\ncan be customized in a ``[tool.jgt_tools]``\nin your ``pyproject.toml`` file.\nAvailable values are:\n\n- ``env_setup_commands`` - a list of commands to be run\n  under the ``env-setup`` call\n- ``self_check_commands`` - a list of commands to be run\n  under the ``self-check`` call\n- ``run_tests_commands`` - a list of commands to be run\n  under the ``run-tests`` call\n- ``doc_build_types`` - a list of types for doc construction:\n  - ``api`` is currently the only supported option\n\nFor example::\n\n    [tool.jgt_tools]\n    env_setup_commands = [\n        "poetry install",\n        "poetry run pip install other_package",\n        "./my_custom_setup_script.sh"\n    ]\n    doc_build_types = []\n\nwould run your specified commands for ``env-setup``\nand skip the ``api`` doc builder.\n\nIn addition,\nthe function to verify which files are relevant to ``check-version``\ncan be customized.\nBy default, if any files in the diff against master are ``.py`` files,\na version bump is expected,\nbut the user can provide an alternate function to verify filenames.\n\nThe function should expect a list of strings\nrepresenting file paths relative from project root\n(as provided by ``git diff master --name-only``)\nand return a boolean representing if a version change should be ensured\n(i.e. ``True`` if version should be checked).\n\nThis can be registered as a plugin in your ``pyproject.toml`` file::\n\n    [tools.poetry.plugins."file_checkers"]\n    "version_trigger" = "my_module:my_function"\n\nor in your ``setup.py`` file::\n\n    setup(\n        ...\n        entry_points={\n            "version_trigger": ["version_trigger = my_module:my_fuction"]\n        }\n    )\n\n.. _`Sphinx site`: http://www.sphinx-doc.org/en/master/usage/quickstart.html#defining-document-structure\n',
    'author': 'Brad Brown',
    'author_email': 'brad@bradsbrown.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://jolly-good-toolbelt.github.io/jgt_tools/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
