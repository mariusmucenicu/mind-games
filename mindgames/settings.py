"""
Store commonly used (across the entire project) parameters.

Functions
=========
    check_database: Check whether the database is configured properly in order for the game to work.

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
import logging
import os
import sqlite3

# Third-party
import web

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TEMPLATES_PATH = os.path.join(BASE_DIR, 'templates')
base_render = web.template.render(TEMPLATES_PATH, base='layout')

DB_TABLE_SCHEMAS = {
    'sessions': (
        'create table sessions ('
        'session_id char(128) UNIQUE NOT NULL, '
        'atime timestamp NOT NULL default current_timestamp, '
        'data text'
        ');'
    )
}


def _check_table(cursor, table):
    # Check if the requested table exists in the current db and whether it has the expected columns.
    table_exists = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' and name='{0}'".format(table)
    ).fetchone()

    if not table_exists:
        logger.debug('Table <{0}> does not exist. Creating..'.format(table))
        raise sqlite3.OperationalError()
    else:
        table_info = cursor.execute('PRAGMA table_info({0})'.format(table)).fetchall()

        for column_definition in table_info:
            column_name = column_definition[1]
            column_not_found_error = (
                '<{0}> column not found in <{1}> table.'.format(column_name, table)
            )
            assert column_name in DB_TABLE_SCHEMAS[table], column_not_found_error

def check_database():
    """Check the database for its core tables, columns in order for the game to work properly."""
    connection = sqlite3.connect('mindgames.db')  # connects to an existing db or creates one
    cursor = connection.cursor()

    try:
        for table in DB_TABLE_SCHEMAS:
            _check_table(cursor, table)
    except sqlite3.OperationalError:
        cursor.execute(DB_TABLE_SCHEMAS[table])
    except AssertionError as e:
        logger.debug('{0} {1}'.format(e, 'Recreating table..'))
        cursor.execute('DROP TABLE {0}'.format(table))
        cursor.execute(DB_TABLE_SCHEMAS[table])
    else:
        logger.info('Database is in normal parameters')
    finally:
        connection.close()
