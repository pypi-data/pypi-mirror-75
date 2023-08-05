JGT Tools
=========

JGT Tools is a collection of package helpers
for common CLI functions
within a properly-formatted repository.


Quickstart
----------

Just include ``jgt_tools`` in your package VirtualEnv,
and you'll have access to these CLI calls:

- ``env-setup`` - set up the development environment
  with all packages and pre-commit checks
- ``self-check`` - run self-checks/linters/etc. on your repository
- ``run-tests`` - run your in-repo test suite
- ``build-docs`` - build repo documentation locally
- ``build-and-push-docs`` - both build the docs,
  then publish to your gh-pages branch
- ``check-version`` - raise an error if package-relevant files have changed
  without a version bump

Details for each script can be found by calling with the ``--help`` flag.


Documentation Index
-------------------

In order to get the full benefit from ``build-docs``,
it is encouraged to create an index file
that pulls together all the documentation.
This file needs to be in the root folder
and should be called ``.jgt_tools.index``.
This will be moved into the working directory for Sphinx
and be used when building the documentation.
Additional information can be found on the `Sphinx site`_.

Configuration
-------------

A number of the actions to be called
can be customized in a ``[tool.jgt_tools]``
in your ``pyproject.toml`` file.
Available values are:

- ``env_setup_commands`` - a list of commands to be run
  under the ``env-setup`` call
- ``self_check_commands`` - a list of commands to be run
  under the ``self-check`` call
- ``run_tests_commands`` - a list of commands to be run
  under the ``run-tests`` call
- ``doc_build_types`` - a list of types for doc construction:
  - ``api`` is currently the only supported option

For example::

    [tool.jgt_tools]
    env_setup_commands = [
        "poetry install",
        "poetry run pip install other_package",
        "./my_custom_setup_script.sh"
    ]
    doc_build_types = []

would run your specified commands for ``env-setup``
and skip the ``api`` doc builder.

In addition,
the function to verify which files are relevant to ``check-version``
can be customized.
By default, if any files in the diff against master are ``.py`` files,
a version bump is expected,
but the user can provide an alternate function to verify filenames.

The function should expect a list of strings
representing file paths relative from project root
(as provided by ``git diff master --name-only``)
and return a boolean representing if a version change should be ensured
(i.e. ``True`` if version should be checked).

This can be registered as a plugin in your ``pyproject.toml`` file::

    [tools.poetry.plugins."file_checkers"]
    "version_trigger" = "my_module:my_function"

or in your ``setup.py`` file::

    setup(
        ...
        entry_points={
            "version_trigger": ["version_trigger = my_module:my_fuction"]
        }
    )

.. _`Sphinx site`: http://www.sphinx-doc.org/en/master/usage/quickstart.html#defining-document-structure
