"""
Store commonly used (across the entire project) parameters.

Constants
=========
BASE_DIR: Project root. Build paths inside the project like this: os.path.join(BASE_DIR, ...).
TEMPLATES_PATH: Templates root. Use this when instantiating render objects.

Global variables:
=================
base_render: Use this for rendering templates.

    Example:
        base_render.foo() will render the templates/foo.html template and then wrap it in the
            templates/layout.html template.

Notes
=====
    If you don't want to use the base template for something, just create a second render object
        without the base attribute, like: render_plain = web.template.render(TEMPLATES_PATH)

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

# Standard library
import os

# Third-party
import web

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TEMPLATES_PATH = os.path.join(BASE_DIR, 'templates')
base_render = web.template.render(TEMPLATES_PATH, base='layout')  # pylint: disable=invalid-name
