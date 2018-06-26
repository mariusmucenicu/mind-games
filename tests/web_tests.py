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
import logging
import unittest

# Third-party
from nose import tools
from paste import fixture
from paste import lint

# Project specific
from bin import webapp


def __debug_writer(self, value):  # pylint: disable=unused-argument
    # work-around to ensure prints from web.py framework are not considered exceptions by paste
    if value == '\n':
        return None
    else:
        logging.error('No errors should be written (got: %s)', value)


lint.ErrorWrapper.write = __debug_writer


class TestIndex(unittest.TestCase):
    def setUp(self):
        self.testApp = fixture.TestApp(webapp.app.wsgifunc())

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
            '...Shh',
        )
        response.mustcontain(*match_items)


class TestGrade(unittest.TestCase):
    def setUp(self):
        self.testApp = fixture.TestApp(webapp.app.wsgifunc())

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
            'Numberphile',
            'Warm up',
            'Numbers are my thing',
            'God blessed my genes'
        )
        response.mustcontain(*match_items)


class TestPlay(unittest.TestCase):
    def setUp(self):
        self.testApp = fixture.TestApp(webapp.app.wsgifunc())

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
        self.testApp = fixture.TestApp(webapp.app.wsgifunc())

    def test_result_correct(self):
        post_data = {
            'left_glyph': '[',
            'right_glyph': ')',
            'start_internal': 0,
            'stop_internal': 99,
            'start_representation': '0',
            'stop_representation': '99',
            'answer': 99,
            'game_level': 0,
        }
        post_params = {
            'data': str(post_data),
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

    def test_result_correct_repr(self):
        # the answer is incorrect to check the representation of large numbers in groups of 3
        # by rendering the results failure HTML
        post_data = {
            'left_glyph': '[',
            'right_glyph': ')',
            'start_internal': 299792458,
            'stop_internal': 299792459,
            'start_representation': '299 792 458',
            'stop_representation': '299 792 459',
            'answer': 2,
            'game_level': 11,
        }
        post_params = {
            'data': str(post_data),
        }
        response = self.testApp.post('/result', params=post_params)
        tools.assert_equals(response.status, 200)
        match_items = (
            'Incorrect!',
            'Next question',
            "I'm done for today",
            'btn-danger',
            'btn',
            '299 792 458',
            '299 792 459',
            'Your answer',
            'Correct answer',
        )
        response.mustcontain(*match_items)

    def test_result_get_not_allowed(self):
        tools.assert_raises(fixture.AppError, self.testApp.get, '/result')  # this is a 405 raise

    def test_result_incorrect(self):
        post_data = {
            'left_glyph': '[',
            'right_glyph': ')',
            'start_internal': 0,
            'stop_internal': 99,
            'start_representation': '0',
            'stop_representation': '99',
            'answer': 100,
            'game_level': 0,
        }
        post_params = {
            'data': str(post_data),
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

    def test_post_erroneous_data(self):
        bogus_values = (
            ('left_glyph', ']'),
            ('right_glyph', '('),
            ('start_representation', '5'),
            ('answer', 'bogus'),
            ('game_level', ''),
        )
        post_data = {
            'left_glyph': '[',
            'right_glyph': ')',
            'start_internal': 0,
            'stop_internal': 99,
            'start_representation': '0',
            'stop_representation': '99',
            'answer': 99,
            'game_level': 0,
        }
        for bogus_item, bogus_value in bogus_values:
            fresh_post_data = post_data.copy()
            fresh_post_data[bogus_item] = bogus_value
            post_params = {
                'data': str(fresh_post_data),
            }
            tools.assert_raises(fixture.AppError, self.testApp.post, '/result', params=post_params)
