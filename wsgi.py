"""
Kick off the web application.

Notes:
======
    This file contains the code mod_wsgi is executing on startup to get the application object.
    The module CONFIG_PATH points to doesn't exist by default and needs to be created before
        running the application. For details check knowlift/default_settings.py's docstring.

CONSTANTS:
==========
    CONFIG_PATH: The full path to the configuration module.

Global variables:
=================
    application: The Flask application. Acts as a central registry for views, URLs, templates, etc.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

__author__ = 'Marius Mucenicu <marius_mucenicu@yahoo.com>'

# Standard library
import os

# Project specific
import knowlift

from knowlift import default_settings

CONFIG_PATH = os.path.join(default_settings.BASE_DIR, 'knowlift', 'settings.py')
application = knowlift.create_app(CONFIG_PATH)
