# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'HMADP'
copyright = '2022, Lukáš Matthew Čejka'
author = 'Lukáš Matthew Čejka'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# TODO: Following the Sphnix documentation from here: https://www.sphinx-doc.org/en/master/tutorial/narrative-documentation.html
#        make the docs for the project be generated almost automatically.
extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# TODO: Browse for a nicer theme
html_theme = 'bizstyle'
html_static_path = ['_static']
