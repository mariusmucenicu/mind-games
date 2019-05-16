"""
Test model related functionality (integrity of data, relationships between entities, etc.).

Classes:
========
    UserModelTests: Test the user entity with its attrs & relationships in various scenarios.
    CountryModelTests: Test the country entity with its attrs & relationships in various scenarios.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

# Standard library
import unittest

# Third party
import sqlalchemy

from sqlalchemy import exc

# Project specific
import tests

from knowlift import models
from tests import factories


class UserModelTests(unittest.TestCase):
    """
    Methods:
    ========
        test_select_user()
        test_update_user()
        test_create_duplicate_values_for_unique_fields_forbidden()
        test_update_duplicate_values_for_unique_fields_forbidden()
        test_create_when_required_fields_are_missing()
        test_create_user_in_different_country()
        test_methods_in_docstring()
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        engine = tests.TEST_APPLICATION.config['DATABASE_ENGINE']
        cls.connection = engine.connect()

    def setUp(self):
        super().setUp()
        self.user = factories.create_user(self.connection)

    def test_select_user(self):
        query = models.user.select(models.user.c.id == self.user.id)
        result = self.connection.execute(query).first()
        self.assertEqual(result.id, self.user.id)

    def test_update_user(self):
        update_values = {
            'username': 'TreeOfLife', 'email': 'tol@knolift.com', 'password': 'Yggdrasil'
        }
        update_query = models.user.update(models.user.c.id == self.user.id, update_values)
        update_result = self.connection.execute(update_query)
        select_query = models.user.select(models.user.c.username == update_values['username'])
        select_result = self.connection.execute(select_query)
        self.assertEqual(update_result.rowcount, 1)
        self.assertIsNotNone(select_result.first())

    def test_create_duplicate_values_for_unique_fields_forbidden(self):
        test_fields = ('username', 'email')
        for test_field in test_fields:
            payload = {test_field: getattr(self.user, test_field)}
            self.assertRaises(
                exc.IntegrityError, factories.create_user, self.connection, **payload
            )

    def test_update_duplicate_values_for_unique_fields_forbidden(self):
        test_fields = ('username', 'email')
        user = factories.create_user(self.connection)
        for test_field in test_fields:
            payload = {test_field: getattr(self.user, test_field)}
            update_duplicate_query = models.user.update(models.user.c.id == user.id, payload)
            self.assertRaises(exc.IntegrityError, self.connection.execute, update_duplicate_query)

    def test_create_when_required_fields_are_missing(self):
        non_nullable_fields = ('username', 'email', 'password', 'country_id')
        for non_nullable_field in non_nullable_fields:
            payload = {non_nullable_field: None}
            self.assertRaises(exc.IntegrityError, factories.create_user, self.connection, **payload)

    def test_create_user_in_different_country(self):
        payload = {'name': 'Australia', 'alpha2_code': 'AU', 'alpha3_code': 'AUS'}
        country_select = models.country.select(models.country.c.name == payload['name'])
        self.assertIsNone(self.connection.execute(country_select).first())

        user = factories.create_user(self.connection, **payload)
        select_columns = [
            models.user.c.username,
            models.country.c.name,
            models.country.c.alpha2_code,
            models.country.c.alpha3_code,
        ]
        query = sqlalchemy.select(
            select_columns,
            models.user.c.username == user.username,
            models.user.join(models.country, models.user.c.id == models.country.c.id)
        )
        result = self.connection.execute(query).first()
        self.assertTrue(all(payload[key] == getattr(result, key) for key in payload.keys()))

    def test_methods_in_docstring(self):
        methods_to_check = [
            method_name for method_name in dir(self) if method_name.startswith('test')
        ]
        for method_to_check in methods_to_check:
            msg = f'{method_to_check} not found in docstring.'
            self.assertIn(method_to_check, self.__doc__, msg)

    def tearDown(self):
        select_query = sqlalchemy.select([sqlalchemy.func.count()]).select_from(models.user)
        count_result = self.connection.execute(select_query).first()
        delete_query = models.user.delete()
        delete_result = self.connection.execute(delete_query)
        self.assertEqual(count_result.count_1, delete_result.rowcount)
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()


class CountryModelTests(unittest.TestCase):
    """
    Methods
    =======
        test_select_country()
        test_update_country()
        test_create_duplicate_values_for_unique_fields_forbidden()
        test_update_duplicate_values_for_unique_fields_forbidden()
        test_methods_in_docstring()
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        engine = tests.TEST_APPLICATION.config['DATABASE_ENGINE']
        cls.connection = engine.connect()

    def setUp(self):
        super().setUp()
        self.country = factories.create_country(self.connection)

    def test_select_country(self):
        query = models.country.select(models.country.c.id == self.country.id)
        result = self.connection.execute(query).first()
        self.assertEqual(result.id, self.country.id)

    def test_create_duplicate_values_for_unique_fields_forbidden(self):
        test_fields = {
            'name': 'United States of America', 'alpha2_code': 'US', 'alpha3_code': 'USA'
        }
        # When we're popping a value, we're using the default value from the factory for that value
        for key, value in test_fields.items():
            test_fields_copy = dict(test_fields)
            test_fields_copy.pop(key)
            self.assertRaises(
                exc.IntegrityError, factories.create_country, self.connection, **test_fields_copy
            )

    def test_update_country(self):
        update_values = {
            'name': 'United States of America', 'alpha2_code': 'US', 'alpha3_code': 'USA'
        }
        update_query = models.country.update(models.country.c.id == self.country.id, update_values)
        update_result = self.connection.execute(update_query)
        select_query = models.country.select(models.country.c.name == update_values['name'])
        select_result = self.connection.execute(select_query).first()
        self.assertEqual(update_result.rowcount, 1)
        self.assertIsNotNone(select_result)

    def test_update_duplicate_values_for_unique_fields_forbidden(self):
        new_country_values = {
            'name': 'United States of America', 'alpha2_code': 'US', 'alpha3_code': 'USA'
        }
        country = factories.create_country(self.connection, **new_country_values)
        for field in self.country.keys():
            payload = {field: getattr(self.country, field)}
            update_duplicate_query = models.country.update(
                models.country.c.id == country.id, payload
            )
            self.assertRaises(exc.IntegrityError, self.connection.execute, update_duplicate_query)

    def test_methods_in_docstring(self):
        methods_to_check = [
            method_name for method_name in dir(self) if method_name.startswith('test')
        ]
        for method_to_check in methods_to_check:
            msg = f'{method_to_check} not found in docstring.'
            self.assertIn(method_to_check, self.__doc__, msg)

    def tearDown(self):
        select_query = sqlalchemy.select([sqlalchemy.func.count()]).select_from(models.country)
        count_result = self.connection.execute(select_query).first()
        delete_query = models.country.delete()
        delete_result = self.connection.execute(delete_query)
        self.assertEqual(count_result.count_1, delete_result.rowcount)
        super().tearDown()

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()
