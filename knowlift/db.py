"""
Store functionality that deals with the underlying database.

Functions:
==========
    close_connection: Close the DB API connection.
    get_connection: Get or create a single DB API connection.
    init_db: Initialize the database.


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

# Project specific
from knowlift import models

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
        logger.error(exception)

    db = getattr(flask.g, 'db', None)
    if db is not None:
        db.close()
    else:
        logger.debug('The database does not exist on the application context.')


def init_db(engine):
    """
    Initialize the database.

    Notes
    =====
    This procedure creates the tables associated to the metadata in knowlift.models.metadata. The
        metadata (and hence the tables associated to it) are bound to an engine.

    The engine should be thought of as something abstract (something that provides database
        connectivity and behavior). Usually the engine is created via a URL (just a string, really)
        that indicates a particular database dialect and connection argument. For instance, the
        tests and production instantiate the engine via different URLs (as they use different dbs).

    This procedure is safe to be called multiple times, as, by default, will not attept to recreate
        tables already present in the target database.

    :param engine: The home base for the actual database and its DBAPI.
    :type engine: sqlalchemy.engine.base.Engine
    """
    models.metadata.create_all(bind=engine)
    engine_metadata = (
        f'Engine Name: "{engine.name}", '
        f'Engine Driver: "{engine.driver}", '
        f'Engine URL: "{engine.url}"'
    )
    logger.debug(f'{engine_metadata}')
