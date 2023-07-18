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
copyright = '2023, Lukáš Matthew Čejka'
author = 'Lukáš Matthew Čejka'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "nature"
html_style = "nature_override.css"

html_static_path = ['_static']

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    "**": [
        "site_custom_sidebars.html",
        "localtoc.html",
        "searchbox.html",
        "relations.html",
    ]
}
