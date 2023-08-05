# Config for Sphinx documentation of Proclamation
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2020 Collabora, Ltd. and the Proclamation contributors

# Documentation builds require the following modules in addition to sphinx:
# recommonmark click sphinx_click sphinx-jsonschema

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

project = 'Proclamation'
copyright = '2019-2020, Collabora, Ltd. and the Proclamation contributors'
author = 'Ryan Pavlik'

version = '1.0'
release = '1.0.2.2'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx.ext.extlinks',
    'recommonmark',
    'sphinx_click.ext',
    'sphinx-jsonschema',
]

source_suffix = ['.rst', '.md']

master_doc = 'index'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

intersphinx_mapping = {'https://docs.python.org/': None}
