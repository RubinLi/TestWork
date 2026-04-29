# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# from enika.version import __version__
from pathlib import Path
import sys
import os
project = 'testwork'
copyright = '2026, Rox'
author = 'Rox'


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_theme = 'classic'
html_static_path = ['_static']
html_theme_options = {
    #    "rightsidebar": "true",
    #    "relbarbgcolor": "black",
    "sidebarwidth": "21%",
    "sidebarbgcolor": "#ad510a",
}
# from enika import version
# sys.path.insert(0, os.path.abspath('..'))
# sys.path.insert(0, str(Path('..', 'src').resolve()))
# basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# sys.path.insert(0, basedir)

sys.path.insert(0, os.path.abspath(
    os.path.join("../../src/testWork/")))
