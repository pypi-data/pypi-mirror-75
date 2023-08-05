"""Sphinx conf.py template."""
CONF_PY = '''
"""Configure sphinx for package doc publication."""
import os

import jgt_tools.utils

# General information about your project.
project = "{name}"
copyright = "{year}, {authors}"  # noqa
author = "{authors}"
release = version = "{version}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    {type_hints}
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.inheritance_diagram",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

html_theme_options = {{
    "style_external_links": True,
    "titles_only": False,
    "collapse_navigation": False,
}}

{markdown}

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".tox",
    "*/.tox",
    ".eggs",
    "*/.eggs",
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# Include both class and init docstrings
autoclass_content = "both"


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

# If anyone wants to use another theme, they can change that here,
# but we consider that expert Sphinx user territory.
import sphinx_rtd_theme  # noqa

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]


commit_id = os.environ.get("ghprbPullId") or os.environ.get("GIT_COMMIT_ID")
base_url = os.environ.get("ghprbPullLink") or ""
if not base_url:
    owner_name = jgt_tools.utils.owner_name_from(os.environ.get("GIT_ORIGIN_URL", ""))
    if owner_name:
        base_url = f"https://github.com/{{owner_name}}/tree/{{commit_id}}"
html_context = {{"build_id": commit_id, "build_url": base_url}}
'''

MARKDOWN = """
from recommonmark.parser import CommonMarkParser  # noqa

source_parsers = {".md": CommonMarkParser}
source_suffix = [".rst", ".md"]
"""

TYPE_HINTS = '"sphinx_autodoc_typehints",'
