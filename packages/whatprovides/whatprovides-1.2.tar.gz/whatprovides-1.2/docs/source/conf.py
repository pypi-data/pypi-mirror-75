# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

# -- Project information -----------------------------------------------------

project = 'whatprovides'
copyright = '2020, shmakovpn'
author = 'shmakovpn'

SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR: str = os.path.dirname(SCRIPT_DIR)
PROJECT_DIR: str = os.path.dirname(DOCS_DIR)
PACKAGE_DIR: str = os.path.join(PROJECT_DIR, project)
sys.path.insert(0, PACKAGE_DIR)

# mocking C modules
# autodoc_mock_imports = []

# reading version information
VERSION: str = ''
with open(os.path.join(PACKAGE_DIR, 'version.py')) as version_file:
    exec(version_file.read())

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']