"""
Handle incoming requests, after being dispatched to the appropriate view by web.py.

Classes:
========
    Index: Get the homepage.
    About: Get the about page.
    FundRaising: Get the fundraising page (contains credits to donors or supporters of any kind).
    Grade: Get the grade (difficulty levels) page.
    Ladder: Get the ladder page.
    Legal: Get the legal page (this page comprises legal information e.g GDPR, terms of use, etc).
    Play: Start the game.
    Result: Return result based on user input.
    RequestHandler: Store configurations for views.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

# Standard library
import logging
import json

# Third-party
import web

# Project specific
from mindgames import number_distance
from mindgames import settings

logger = logging.getLogger(__name__)


class RequestHandler:
    def __init__(self):
        self.session = web.config.get('_session') or {}

    def _update_user_statistics(self, game_metadata):
        if not self.session:
            return
        elif game_metadata['outcome']:
            self.session['correct_answers'] += 1
        else:
            self.session['incorrect_answers'] += 1

        self.session['total_answers'] += 1
        last_average = self.session['correct_answers'] + self.session['incorrect_answers']

        if last_average == self.session['average']:
            self._change_game_level(game_metadata)
            self._reset_user_statistics()
        else:
            logger.debug('Skipping reset statistics')

    def _reset_user_statistics(self):
        self.session['correct_answers'] = 0
        self.session['incorrect_answers'] = 0

    def _change_game_level(self, game_metadata):
        correct_answers = self.session['correct_answers']
        incorrect_answers = self.session['incorrect_answers']
        current_game_level = game_metadata['game_level']
        new_game_level = number_distance.change_game_level(
            correct_answers, incorrect_answers, current_game_level
        )
        game_metadata['game_level'] = new_game_level

    def clear_session(self):
        self.session.kill()


class Index:
    """
    Methods:
    ========
        GET()
    """

    def GET(self):
        return settings.base_render.index()


class About:
    """
    Methods:
    ========
        GET()
    """

    def GET(self):
        return settings.base_render.about()


class FundRaising:
    """
    Methods:
    ========
        GET()
    """

    def GET(self):
        return settings.base_render.fundraising()


class Grade:
    """
    Methods:
    ========
        GET()
    """

    def GET(self):
        return settings.base_render.grade()


class Ladder:
    """
    Methods:
    ========
        GET()
    """

    def GET(self):
        return settings.base_render.ladder()


class Legal:
    """
    Methods:
    ========
        GET()
    """

    def GET(self):
        return settings.base_render.legal()


class Play:
    """
    Methods:
    ========
        POST()
    """

    def POST(self):
        level = web.input().get('level')
        if not level:
            raise web.seeother('/grade')
        else:
            data = number_distance.play(level)
            if not data:
                raise web.internalerror()
            else:
                return settings.base_render.play(data)


class Result(RequestHandler):
    """
    Methods:
    ========
        POST()
    """

    def POST(self):
        data_to_dict = json.loads(web.input().get('data'))
        result_data = number_distance.generate_results(data_to_dict)

        if not result_data:
            raise web.internalerror()
        elif result_data['outcome']:
            self._update_user_statistics(result_data)
            return settings.base_render.result_correct(result_data)
        else:
            self._update_user_statistics(result_data)
            return settings.base_render.result_incorrect(result_data)
