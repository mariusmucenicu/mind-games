"""
Store environment-based configuration (development, production, test).

Classes:
========
    Config: Store the default configuration settings. Override per-subclass.
    DevelopmentConfig: Store the development configuration settings.
    ProductionConfig: Store the production configuration settings.
    TestConfig: Store the test configuration settings.
    ConsoleFilter: Filter out LogRecords whose levels are > logging.WARNING
    FileFilter: Filter out LogRecords whose levels are < logging.ERROR

Notes
=====
    * These settings are required to be available when the application starts up.
    * Many of these settings are sensitive and should be treated as confidential.
    * There is a different configuration available for each main environment (prod, dev, test):
    * The environments above are used to indicate to Flask what context the app is running in.
    * To switch between environments (configurations) set the FLASK_ENV environment variable to any
        of the configuration's prefixes: 'production', 'development' or 'test'. FLASK_ENV is set
        automatically to 'test' from within Python during test mode, regardless of what its value is
        at the OS level. One shouldn't set FLASK_ENV to 'test' at the OS level, unless, for some
        reason, one wants to run the application on purpose with the TestConfig.
    * If FLASK_ENV is not set, the default configuration used will be the ProductionConfig.
    * Do not alter settings in the application at runtime. For example, don't do things like:
        flask.current_app.config['DEBUG'] = True

Changes to this module
======================
    - Changes to this module should only be submitted through a formal process (via PR's).

Altering settings locally
=========================
    - Any customization to should be done locally, outside the VCS via the instance folder.
    - The instance folder does not exist by default and its ignored by git.
    - The process of altering settings locally is as follows:
        1. Create the instance folder in the project root, i.e, at the same level as this module.
        2. Create a module named 'settings.py' inside the instance folder created at step 1.
        3. Alter any settings there.

        For example, to use a different SECRET_KEY simply add SECRET_KEY = 'new crypto value'
            in that module (instance/settings.py), globally.

    - The application loads the default settings and overrides them with any settings found in
        instance/settings.py.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

# Standard library
import logging
import os


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


class Config:
    """Store the default configuration. Override these values in subclasses per-environment."""

    # Whether debug mode is enabled. This is overridden by the FLASK_DEBUG environment variable.
    # DO NOT ENABLE DEBUG MODE WHEN DEPLOYING IN PRODUCTION!
    DEBUG = False

    # Whether testing mode is enabled. Exceptions are propagated rather than handled by Flask.
    TESTING = False

    # Absolute path to the project root on the filesystem.
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # The absolute pathname of the database file to be opened.
    DATABASE = os.path.join(BASE_DIR, 'default.db')

    # The secret key is used to provide cryptographic signing (e.g used to sign Cookies).
    # SECURITY WARNING: Set this to some random bytes. Keep this value secret in production!
    SECRET_KEY = os.urandom(32).hex()

    # Initial configuration for the logging machinery.
    LOGGING_CONFIG = {
        'version': 1,
        'formatters': {
            'default': {
                'format': f'[%(asctime)s] %(levelname)s in %(module)s, line %(lineno)d: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
        },
        'loggers': {
            'knowlift': {
                'level': 'DEBUG',
                'handlers': ['default'],
                'propagate': False,
            },
            'sqlalchemy': {
                'level': 'DEBUG',
                'handlers': ['default'],
                'propagate': False,
            },
            'werkzeug': {
                'level': 'DEBUG',
                'handlers': ['default'],
                'propagate': False,
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['default'],
        },
    }


class ProductionConfig(Config):
    """
    Store the production configuration.

    Check the BaseClass for additional information on individual settings.
    """

    DEBUG = False
    TESTING = False
    DATABASE = os.path.join(Config.BASE_DIR, 'production.db')
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', Config.SECRET_KEY)
    LOGGING_CONFIG = {
        'version': 1,
        'formatters': {
            'default': {
                'format': f'[%(asctime)s] %(levelname)s in %(module)s, line %(lineno)d: %(message)s'
            },
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
            'default': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
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
                'level': 'WARNING',
                'handlers': ['console', 'file'],
                'propagate': False,
            },
            'sqlalchemy': {
                'level': 'WARNING',
                'handlers': ['console', 'file'],
                'propagate': False,
            },
            'werkzeug': {
                'level': 'WARNING',
                'handlers': ['console', 'file'],
                'propagate': False,
            },
        },
        'root': {
            'level': 'WARNING',
            'handlers': ['default'],
        },
    }


class DevelopmentConfig(Config):
    """
    Store the development configuration.

    Check the BaseClass for additional information on individual settings.
    """

    DEBUG = True
    TESTING = False
    DATABASE = os.path.join(Config.BASE_DIR, 'development.db')
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', Config.SECRET_KEY)
    LOGGING_CONFIG = {
        'version': 1,
        'formatters': {
            'default': {
                'format': f'[%(asctime)s] %(levelname)s in %(module)s, line %(lineno)d: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
        },
        'loggers': {
            'knowlift': {
                'level': 'WARNING',
                'handlers': ['default'],
                'propagate': False,
            },
            'sqlalchemy': {
                'level': 'WARNING',
                'handlers': ['default'],
                'propagate': False,
            },
            'werkzeug': {
                'level': 'DEBUG',
                'handlers': ['default'],
                'propagate': False,
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['default'],
        },
    }


class TestConfig(Config):
    """
    Store the test configuration.

    Check the BaseClass for additional information on individual settings.
    """

    DEBUG = False
    TESTING = True
    DATABASE = os.path.join(Config.BASE_DIR, 'test.db')
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', Config.SECRET_KEY)
    LOGGING_CONFIG = {
        'version': 1,
        'formatters': {
            'default': {
                'format': f'[%(asctime)s] %(levelname)s in %(module)s, line %(lineno)d: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
        },
        'loggers': {
            'knowlift': {
                'level': 'WARNING',
                'handlers': ['default'],
                'propagate': False,
            },
            'sqlalchemy': {
                'level': 'WARNING',
                'handlers': ['default'],
                'propagate': False,
            },
            'werkzeug': {
                'level': 'WARNING',
                'handlers': ['default'],
                'propagate': False,
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['default'],
        },
    }
