import os
import sys
sys.path.insert(0, os.path.abspath('../../packages/recipe_core/src'))

project = 'Recipe KBZhU Calculator'
copyright = '2026, Student'
author = 'Student'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'myst_parser'
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']
