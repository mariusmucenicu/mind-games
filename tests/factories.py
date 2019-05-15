"""
Implement model factories that will aid in respecting the DRY principle throughout tests.

Functions
=========
    country_factory: Create an instance of a country entity in the database.
    user_factory: Create an instance of a user entity in the database.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

# Project specific
from knowlift import models


def user_factory(connection, **kwargs):
    """
    Create a user record in the database.

    :param connection: A single DBAPI connection checked out from the connection pool.
    :type connection: sqlalchemy.engine.base.Connection
    :param kwargs: A collection of values that a user model can accept.
    :type kwargs: dict
    :return: Proxy values for our newly created user.
    :rtype: sqlalchemy.engine.result.RowProxy
    """
    country = country_factory(connection)
    user_values = {
        'username': 'j&j',
        'first_name': 'Jack',
        'last_name': 'Jones',
        'email': 'jack.jones@knowlift.com',
        'password': 'storm_breaker',
        'country_id': country['id'],
    }
    user_values.update(**kwargs)

    # insert
    insert_query = models.user.insert(values=user_values)
    connection.execute(insert_query)

    # select
    select_query = models.user.select()
    result = connection.execute(select_query)
    return result.fetchone()


def country_factory(connection, **kwargs):
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
        'name': 'Romania',
        'alpha2_code': 'RO',
        'alpha3_code': 'ROU'
    }
    country_values.update(**kwargs)

    # insert
    insert_query = models.country.insert(values=country_values)
    connection.execute(insert_query)

    # select
    select_query = models.country.select()
    result = connection.execute(select_query)
    return result.fetchone()
