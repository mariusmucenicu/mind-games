"""
Test bin.webapp functionality.

Classes:
========
    TestIndexPage: Test the requests going under /index
    TestAboutPage: Test the requests going under /about
    TestCustomInternalErrorPage: Test the requests that the server failed to fulfil
    TestCustomNotFoundPage: Test the requests that are not mapped to any url
    TestFundraisingPage: Test the requests going under /fundraising
    TestGradePage: Test the requests going under /grade
    TestLadderPage: Test the requests going under /ladder
    TestLegalPage: Test the requests going under /legal
    TestPlayPage: Test the requests going under /play
    TestResultPage: Test the requests going under /result
"""

# Standard library
import json
import logging
import unittest

# Third-party
from nose import tools
from paste import fixture
from paste import lint

# Project specific
from bin import webapp

logger = logging.getLogger(__name__)


def __debug_writer(self, value):  # pylint: disable=unused-argument
    # work-around to ensure prints from web.py framework are not considered exceptions by paste
    if value == '\n':
        return None
    else:
        logger.error('No errors should be written (got: %s)', value)


lint.ErrorWrapper.write = __debug_writer


class TestIndexPage(unittest.TestCase):
    def setUp(self):
        self.testApp = fixture.TestApp(webapp.app.wsgifunc())

    def test_get_index_page(self):
        response = self.testApp.get('/')
        tools.assert_equals(response.status, 200)
        match_items = (
            'Welcome to the fascinating world of arithmetic',
            'This game aims to mimic the behavior of an abacus',
            'open interval',
            'closed interval',
            'half-open interval',
            'container-fluid d-flex flex-column',
            'd-flex flex-column justify-content-center',
            '...Shh',
            'A pit stop for your brain.',
            'Version 0.1.0',
            'header',
            'content',
            'footer',
            'https://www.w3.org/TR/html/',
            'https://www.w3.org/TR/CSS/',
            'https://www.w3schools.com/js/js_versions.asp',
            'https://www.python.org/',
            'Connect with the author:',
            'twitter',
            'instagram',
            'linkedin',
            'github',
        )
        response.mustcontain(*match_items)


class TestAboutPage(unittest.TestCase):
    def setUp(self):
        self.testApp = fixture.TestApp(webapp.app.wsgifunc())

    def test_get_about_page(self):
        response = self.testApp.get('/about')
        tools.assert_equals(response.status, 200)
        match_items = (
            'About',
            '/about',  # tests the href in the header of the layouts base template
            'coming_soon',
        )
        response.mustcontain(*match_items)


class TestCustomNotFoundPage(unittest.TestCase):
    def setUp(self):
        self.testApp = fixture.TestApp(webapp.app.wsgifunc())

    def test_get_custom_not_found_page(self):
        response = self.testApp.get('/bogus', status=404)  # non-existent page
        match_items = (
            'Oops! It looks like',
            "Looks like you followed a bad path. If you think it's the author's fault",
            'Below you will find two helpful links. You know, just in case.',
            'Home page',
            "Nah bruh. I'm outta here!",
            'type="image/webp"',
            'detective_slim.webp',
            'detective.jpg',
        )
        response.mustcontain(*match_items)


class TestFundraisingPage(unittest.TestCase):
    def setUp(self):
        self.testApp = fixture.TestApp(webapp.app.wsgifunc())

    def test_get_fundraising_page(self):
        response = self.testApp.get('/fundraising')
        tools.assert_equals(response.status, 200)
        match_items = (
            'Fundraising',
            '/fundraising',
            'coming_soon.jpg',
        )
        response.mustcontain(*match_items)


class TestGradePage(unittest.TestCase):
    def setUp(self):
        self.testApp = fixture.TestApp(webapp.app.wsgifunc())

    def test_get_grade_page(self):
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
            'God blessed my genes',
            'd-flex flex-column justify-content-center',
        )
        response.mustcontain(*match_items)


class TestCustomInternalErrorPage(unittest.TestCase):
    def setUp(self):
        self.testApp = fixture.TestApp(webapp.app.wsgifunc())

    def test_yield_custom_internal_error_page(self):
        post_data = {
            'left_glyph': '[',
            'right_glyph': ')',
            'start_internal': 0,
            'stop_internal': 99,
            'start_representation': '0',
            'stop_representation': '99',
            'answer': 'bogus',  # only integers allowed
            'game_level': 0,
        }
        post_params = {
            'data': json.dumps(post_data),
        }
        response = self.testApp.post('/result', params=post_params, status=500)
        match_items = (
            'Oops! It looks like',
            "Try that again, and if it still doesn't work",
            'Below you will find two helpful links. You know, just in case.',
            'Home page',
            "Nah bruh. I'm outta here!",
            'type="image/webp"',
            'dinosaur_slim.webp',
            'dinosaur.jpg',
        )
        response.mustcontain(*match_items)


class TestLadderPage(unittest.TestCase):
    def setUp(self):
        self.testApp = fixture.TestApp(webapp.app.wsgifunc())

    def test_get_ladder_page(self):
        response = self.testApp.get('/ladder')
        tools.assert_equals(response.status, 200)
        match_items = (
            'Ladder',
            '/ladder',
            'coming_soon.jpg',
        )
        response.mustcontain(*match_items)


class TestLegalPage(unittest.TestCase):
    def setUp(self):
        self.testApp = fixture.TestApp(webapp.app.wsgifunc())

    def test_get_legal_page(self):
        response = self.testApp.get('/legal')
        tools.assert_equals(response.status, 200)
        match_items = (
            'border-stretch',
            'contents',
            'contents__item',
            'contents__link',
            'legal__terms_conditions',
            'legal__liability',
            'legal__litigation',
            'legal__privacy_policy',
            'legal__data_security',
            'legal__do_not_track',
            'legal__cookie_policy',
            'legal__cookie_types',
            'legal__cookie_usage',
            'legal__cookie_ctrl',
            'legal__cookie_further_reading',
            'legal__additional_info',
            'legal__history_of_software',
            'legal__license',
            'legal__useful_links',
            'fa-chevron-circle-up',
            'marius_mucenicu@yahoo.com',
            'mariusmucenicu',
            'Marius Mucenicu',
            'scrollToElement',
        )
        response.mustcontain(*match_items)


class TestPlayPage(unittest.TestCase):
    def setUp(self):
        self.testApp = fixture.TestApp(webapp.app.wsgifunc())

    def test_get_not_allowed(self):
        tools.assert_raises(fixture.AppError, self.testApp.get, '/play')  # 405 Method not allowed

    def test_play_post_with_no_value(self):
        response = self.testApp.post('/play')
        tools.assert_equals(response.status, 303)

    def test_play_post_with_incorrect_value(self):
        tools.assert_raises(fixture.AppError, self.testApp.post, '/play', params={'level': 'a'})
        tools.assert_raises(fixture.AppError, self.testApp.post, '/play', params={'level': 12})

    def test_play_post_valid_data(self):
        response = self.testApp.post('/play', params={'level': 0})
        match_items = (
            'Hit it',
            "I'm feeling lucky",
            'How many integers are within this interval ?',
            'd-flex flex-column justify-content-center',
            'checkEmptyInput',
            'processFormData',
            'clearFormField',
            'fa-times',
            'fa-search',
            'metadata',
            'play-form',
            'form-play',
            'roulette',
            'clearSearch',
            'play-form__input',
            'form-play__button',
            'form-play__button--glass',
            'form-play__button--toggle',
        )
        response.mustcontain(*match_items)


class TestResultPage(unittest.TestCase):
    def setUp(self):
        self.testApp = fixture.TestApp(webapp.app.wsgifunc())

    def test_post_result_correct_answer(self):
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
            'data': json.dumps(post_data),
        }
        response = self.testApp.post('/result', params=post_params)
        tools.assert_equals(response.status, 200)
        match_items = (
            'Correct!',
            'Next question',
            "I'm done for today",
            'd-flex flex-column justify-content-center',
        )
        response.mustcontain(*match_items)

    def test_post_result_correct_representation(self):
        # the answer is incorrect to check the representation of large numbers in groups of 3
        # by rendering the results_incorrect.html
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
            'data': json.dumps(post_data),
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

    def test_post_result_incorrect_answer(self):
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
            'data': json.dumps(post_data),
        }
        response = self.testApp.post('/result', params=post_params)
        tools.assert_equals(response.status, 200)
        match_items = (
            'Incorrect!',
            'Next question',
            "I'm done for today",
            'd-flex flex-column justify-content-center',
            'Interval',
            'Your answer',
            'Correct answer',
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
