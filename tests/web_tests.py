"""
Test bin.webapp functionality.

Classes:
========
    TestWebApp: Test all public classes within bin.webapp
        For each public class within bin.webapp there is a corresponding test method within the
        tests.web_tests.TestWebApp of the form tests.web_tests.TestWebApp.test_<classname>
        example: bin.webapp.Index is tested by the tests.web_tests.TestWebApp.test_index method.

Notes:
======
    Tests will be split so that each method within TestWebApp becomes a class of its own.
    For the time being, the functionality isn't that complex for the time investment to be worth it.

Miscellaneous objects:
======================
    Except the above, all other objects in this module are to be considered implementation details.
"""

# Standard library
import os
import unittest

# Third-party
from nose import tools
from paste import fixture

# Project specific
from bin import webapp

# this is needed to avoid kicking off the development server during tests
os.environ['WEBPY_ENV'] = 'test'


class TestWebApp(unittest.TestCase):
    def setUp(self):
        middleware = []
        self.testApp = fixture.TestApp(webapp.app.wsgifunc(*middleware))

    def test_index(self):
        response = self.testApp.get('/')
        tools.assert_equals(response.status, 200)
        match_items = (
            'Welcome to the fascinating world of arithmetic',
            'This game aims to mimic the behavior of an abacus',
            'the open interval',
            'the closed interval',
            'the half-open interval',
            'btn-begin',
            'btn-quit',
        )
        response.mustcontain(*match_items)

    def test_grade(self):
        response = self.testApp.get('/grade')
        tools.assert_equals(response.status, 200)
        match_items = (
            'Please choose one of the following difficulties',
            'Easy',
            'Medium',
            'Hard',
            'Use selected',
            'Just pick one for me',
        )
        response.mustcontain(*match_items)

    def test_play(self):
        tools.assert_raises(fixture.AppError, self.testApp.get, '/play')  # this is a 405 raise
        response = self.testApp.post('/play', params={'level': 'a'})
        tools.assert_equals(response.status, 200)
        match_items = (
            'Hit it',
            "I'm feeling lucky",
            'How many integers are within this interval ?',
            'user-answer',
            'hidden',
            'footer',
            'play-form-text',
            'play-form-btn',
        )
        response.mustcontain(*match_items)

    def test_result_correct(self):
        tools.assert_raises(fixture.AppError, self.testApp.get, '/result')  # this is a 405 raise
        post_params = {
            'raw_data': str(
                {
                    'left_glyph': '[',
                    'right_glyph': ')',
                    'left_bound': 0,
                    'right_bound': 99,
                    'start': 59,
                    'stop': 78,
                }
            ),
            'answer': 19,
        }
        response = self.testApp.post('/result', params=post_params)
        tools.assert_equals(response.status, 200)
        match_items = (
            'Correct!',
            'Next question',
            "I'm done for today",
            'btn-success',
            'btn',
        )
        response.mustcontain(*match_items)

    def test_result_incorrect(self):
        tools.assert_raises(fixture.AppError, self.testApp.get, '/result')  # this is a 405 raise
        post_params = {
            'raw_data': str(
                {
                    'left_glyph': '[',
                    'right_glyph': ')',
                    'left_bound': 0,
                    'right_bound': 99,
                    'start': 59,
                    'stop': 78,
                }
            ),
            'answer': 24,
        }
        response = self.testApp.post('/result', params=post_params)
        tools.assert_equals(response.status, 200)
        match_items = (
            'Incorrect!',
            'Next question',
            "I'm done for today",
            'btn-danger',
            'btn'
        )
        response.mustcontain(*match_items)
