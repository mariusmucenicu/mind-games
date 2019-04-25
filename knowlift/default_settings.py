"""
Store the configuration necessary to start the application.

Classes:
========
    ConsoleFilter: Filter out LogRecords whose levels are > logging.WARNING
    FileFilter: Filter out LogRecords whose levels are < logging.ERROR

CONSTANTS
=========
    BASE_DIR: Absolute path to the project root on the filesystem.
    DATABASE: Absolute path to the database on the filesystem.
    DATABASE_ENGINE: A mechanism used to interact with the database.
    LOGGING_CONF: Initial configuration for the logging machinery.
    SECRET_KEY: A value used to create a signature string (used to sign Cookies).

Notes
=====
    TL;DR:
    ------
        * Make a copy of this file and rename it to settings.py in order to run the application.

    Long version:
    -------------
        * These settings are required to be available when the application starts up.
        * The application loads the necessary configuration from a module called settings.py, which,
            by default is not added to the version control system for security and customization
            purposes.

            The purpose of the settings.py module is to hold environment specific settings, such as:
                * production settings (these are the sensitive ones)
                * staging settings
                * development settings

        In order to run the application or override any values found in this module, the drill is:
            1. Make a copy of this file and rename it to settings.py
            2. Override the values as necessary (in settings.py)

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

# Standard library
import logging
import os

# Third-party
import sqlalchemy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE = os.path.join(BASE_DIR, 'default.db')
DATABASE_ENGINE = sqlalchemy.create_engine(f'sqlite:///{DATABASE}')

# SECURITY WARNING: Set the secret key to some random bytes. Keep this really secret in production!
SECRET_KEY = '8bc5150c3f107d9ef1f4b7d1aec03a3721e374d1a992e3cce2d8e57f7338288f'


class ConsoleFilter:
    """Allow only LogRecords whose severity levels are either DEBUG, INFO or WARNING."""

    def __call__(self, log):
        if log.levelno in (logging.DEBUG, logging.INFO, logging.WARNING):
            return 1
        else:
            return 0


class FileFilter:
    """Allow only LogRecords whose severity levels are either ERROR or CRITICAL."""

    def __call__(self, log):
        if log.levelno in (logging.ERROR, logging.CRITICAL):
            return 1
        else:
            return 0


LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': f'[%(asctime)s] %(levelname)s in %(module)s, line %(lineno)d: %(message)s',
        }
    },
    'filters': {
        'file_filter': {
            '()': FileFilter,
        },
        'console_filter': {
            '()': ConsoleFilter,
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'filters': ['console_filter'],
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': 'errors.log',
            'filters': ['file_filter'],
            'maxBytes': 500 * 1024 * 1024,
            'backupCount': 1,
        },
    },
    'loggers': {
        'knowlift': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
        }
    },
}
