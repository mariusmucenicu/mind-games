"""
Store functionality that deals with the underlying database.

Functions:
==========
    get_connection: Get or create a single DB API connection.
    close_connection: Close the DB API connection.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

# Standard library
import logging

# Third-party
import flask

logger = logging.getLogger(__name__)


def get_connection():
    """
    Get or create a single DB API connection checked out from the connection pool.

    :return: A new Connection object.
    :rtype: sqlalchemy.engine.base.Connection
    """
    if 'db' not in flask.g:
        engine = flask.current_app.config['DATABASE_ENGINE']
        flask.g.db = engine.connect()
        return flask.g.db
    else:
        return flask.g.db


def close_connection(exception):
    """Return the underlying DB API connection to the connection pool."""
    if exception:
        logger.debug(exception)

    db = getattr(flask.g, 'db', None)
    if db is not None:
        db.close()
    else:
        logger.debug('The database does not exist on the application context.')
