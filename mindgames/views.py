"""
Handle incoming requests, after being dispatched to the appropriate view by web.py.

Classes:
========
    Index: Get the homepage.
    Grade: Get the grade (difficulty levels) page.
    Play: Start the game.
    Result: Return result based on user input.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

# Standard library
import json

# Third-party
import web

# Project specific
from mindgames import number_distance
from mindgames import settings

# pylint: disable=invalid-name


class Index:
    """
    Methods:
    ========
        GET()
    """

    def GET(self):
        return settings.base_render.index()


class Grade:
    """
    Methods:
    ========
        GET()
    """

    def GET(self):
        return settings.base_render.grade()


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


class Result:
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
            return settings.base_render.result_success(result_data)
        else:
            return settings.base_render.result_failure(result_data)
