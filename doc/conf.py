import os
import sys
sys.path.insert(
    0, 
    os.path.abspath(
        os.path.join('..'))
    )

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'xenharmlib'
copyright = '2024, Fabian Vallon'
author = 'Fabian Vallon'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest']

templates_path = ['_templates']
html_css_files = ['css/smufl.css',]
static_path = ['_static']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_logo = "_static/images/sidebar-logo.png"



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
