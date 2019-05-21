"""
Implement model factories that will aid in respecting the DRY principle throughout tests.

Global variables:
================
    logger: An object that exposes several methods that can be used to log messages at runtime.
    infinite_sequence: An iterator that returns evenly spaced values starting with a number.

Functions
=========
    create_country: Create an instance of a country entity in the database.
    create_user: Create an instance of a user entity in the database.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

# Standard library
import itertools
import logging
import os

# Third party
from sqlalchemy import exc

# Project specific
from knowlift import models

logger = logging.getLogger(__name__)

infinite_sequence = itertools.count(start=1)


def create_user(connection, **kwargs):
    """
    Create a user record in the database.

    :param connection: A single DBAPI connection checked out from the connection pool.
    :type connection: sqlalchemy.engine.base.Connection
    :param kwargs: A collection of values that a user model can accept.
    :type kwargs: dict
    :return: Proxy values for our newly created user.
    :rtype: sqlalchemy.engine.result.RowProxy
    """
    try:
        country = create_country(connection, **kwargs)
    except exc.IntegrityError as ex:
        logger.debug(f'Duplicate entry for country "{ex.params[0]}". Fetching the existing one.')
        select_country = models.country.select(models.country.c.english_short_name == ex.params[0])
        country = connection.execute(select_country).fetchone()

    current_user = next(infinite_sequence)
    user_values = {
        'username': f'JohnWick{current_user}',
        'first_name': 'John',
        'last_name': 'Wick',
        'email': f'jw{current_user}@knowlift.com',
        'password': os.urandom(16).hex(),
        'country_id': country.id,
    }
    user_values.update(pair for pair in kwargs.items() if pair[0] in user_values)

    # insert
    insert_query = models.user.insert(values=user_values)
    connection.execute(insert_query)

    # select
    select_query = models.user.select(models.user.c.username == user_values['username'])
    result = connection.execute(select_query)
    return result.fetchone()


def create_country(connection, **kwargs):
    """
    Create a country record in the database.

    :param connection: A single DBAPI connection checked out from the connection pool.
    :type connection: sqlalchemy.engine.base.Connection
    :param kwargs: A collection of values that a country model can accept.
    :type kwargs: dict
    :return: Proxy values for our newly created user.
    :rtype: sqlalchemy.engine.result.RowProxy
    """
    country_values = {
        'english_short_name': 'Romania',
        'alpha2_code': 'RO',
        'alpha3_code': 'ROU'
    }
    country_values.update(pair for pair in kwargs.items() if pair[0] in country_values)

    # insert
    insert_query = models.country.insert(values=country_values)
    connection.execute(insert_query)

    # select
    where_clause = models.country.c.english_short_name == country_values['english_short_name']
    select_query = models.country.select(where_clause)
    result = connection.execute(select_query)
    return result.fetchone()
