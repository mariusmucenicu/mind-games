"""
Test bin.webapp functionality.

Classes:
========
    TestIndex: Test the requests going under /index
    TestGrade: Test the requests going under /grade
    TestPlay: Test the requests going under /play
    TestResult: Test the requests going under /result


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


class TestIndex(unittest.TestCase):
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


class TestGrade(unittest.TestCase):
    def setUp(self):
        middleware = []
        self.testApp = fixture.TestApp(webapp.app.wsgifunc(*middleware))

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


class TestPlay(unittest.TestCase):
    def setUp(self):
        middleware = []
        self.testApp = fixture.TestApp(webapp.app.wsgifunc(*middleware))

    def test_get_not_allowed(self):
        tools.assert_raises(fixture.AppError, self.testApp.get, '/play')  # 405 Method not allowed

    def test_play_post_with_no_value(self):
        response = self.testApp.post('/play')
        tools.assert_equals(response.status, 303)

    def test_play_post_with_wrong_value(self):
        tools.assert_raises(fixture.AppError, self.testApp.post, '/play', params={'level': 'a'})
        tools.assert_raises(fixture.AppError, self.testApp.post, '/play', params={'level': 12})

    def test_play_post_valid_data(self):
        response = self.testApp.post('/play', params={'level': 0})
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


class TestResult(unittest.TestCase):
    def setUp(self):
        middleware = []
        self.testApp = fixture.TestApp(webapp.app.wsgifunc(*middleware))

    def test_result_correct(self):
        tools.assert_raises(fixture.AppError, self.testApp.get, '/result')  # this is a 405 raise
        raw_data = {
            'left_glyph': '[',
            'right_glyph': ')',
            'left_bound': 0,
            'right_bound': 99,
            'start': 59,
            'stop': 78
        }
        post_params = {
            'raw_data': str(raw_data),
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

    def test_result_get_not_allowed(self):
        tools.assert_raises(fixture.AppError, self.testApp.get, '/result')  # this is a 405 raise

    def test_result_incorrect(self):
        raw_data = {
            'left_glyph': '[',
            'right_glyph': ')',
            'left_bound': 0,
            'right_bound': 99,
            'start': 59,
            'stop': 78,
        }
        post_params = {
            'raw_data': str(raw_data),
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
