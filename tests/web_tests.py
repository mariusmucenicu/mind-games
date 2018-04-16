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


class TestCode(unittest.TestCase):
    def setUp(self):
        middleware = []
        self.testApp = fixture.TestApp(webapp.app.wsgifunc(*middleware))
        templates_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        templates_path = '{0}/templates'.format(templates_dir)
        webapp.render = webapp.web.template.render(templates_path, base='layout')

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
