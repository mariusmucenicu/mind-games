"""
Kick off the web application.

Notes:
======
    This file contains the code mod_wsgi is executing on startup to get the application object.
    The module settings.py doesn't exist by default and needs to be created before running the
        application. For details check knowlift/default_settings.py's docstring.

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

# Project specific
import knowlift

from knowlift import settings

application = knowlift.create_app(settings.__file__)
