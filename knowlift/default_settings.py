"""
Store the configuration necessary to start the application.

CONSTANTS
=========
    BASE_DIR: Absolute path to the project root on the filesystem.
    DATABASE: Absolute path to the database on the filesystem.
    DATABASE_ENGINE: A mechanism used to interact with the database.
    SECRET_KEY: A value used to create a signature string (used to sign Cookies).

Notes
=====
    These settings need to be available when the application starts up.
    The application loads the necessary configuration from 2 objects, as follows:
        1. This module (which holds the default settings), and is added to the version control.
        2. A module called settings.py (if it exists), which is not added to the version control.

        The purpose of the settings.py is to hold environment specific settings, such as:
            * production settings
            * staging settings
            * development settings

        The process of overriding any values found in this module, is a 2-step process, as follows:
            1. A copy of this file should be made and renamed to settings.py
            2. Override the values as necessary (in settings.py)

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

# Standard library
import os

# Third-party
import sqlalchemy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE = os.path.join(BASE_DIR, 'default.db')
DATABASE_ENGINE = sqlalchemy.create_engine(f'sqlite:///{DATABASE}')

# SECURITY WARNING: Set the secret key to some random bytes. Keep this really secret in production!
SECRET_KEY = '8bc5150c3f107d9ef1f4b7d1aec03a3721e374d1a992e3cce2d8e57f7338288f'
