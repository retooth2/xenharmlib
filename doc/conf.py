import os
import sys
from unittest import mock

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
html_extra_path = ['google6d5968067404c332.html']

if 'READTHEDOCS' in os.environ:

    # fake modules with requirements written in C for readthedocs
    # RTD does not install dependencies that have bindings to C
    # code so we need to mock these for generating API docs

    MOCK_MODULES = [
        'numpy',
        'scipy',
        'scipy.optimize',
        'scipy.io',
        'scipy.io.wavfile',
        'sympy',
        'sounddevice',
    ]
    for mod_name in MOCK_MODULES:
        sys.modules[mod_name] = mock.Mock()

    # FIXME: there should be some way to patch Frequency and FrequencyRatio
    # so the default values in the docs do not show as mock.Mock
