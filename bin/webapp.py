"""
Kick off the development server.

Intended for developing purposes (testing the game, adding features, debugging, etc.), rather than
actual serving files on the internet. Should you want to publish the game and have people interact
with it over the internet, you should try to serve files through nginx/apache or a real mature web
server.

Classes:
========
    Index: Get the homepage.
    Grade: Get the grade (difficulty levels) page.
    Play: Start the game.
    Result: Return result based on user input compared against the correct answer.

Miscellaneous objects:
======================
    Except the above, all other objects in this module are to be considered implementation details.

Usage:
======
    python bin/webapp.py [port]

Notes:
======
    Run it from the root folder, not from within bin.
    If you don't specify a port it will default to 8080.
    Create your own personal domain in a few easy steps:
        1. Add 127.0.0.1 <domain_name.extension> to your hosts file, e.g: mucenicu.rocks.
        2. Pop open Chrome/Mozilla Firefox/Opera/etc. punch the domain and enjoy the game.
        3. Careful, if you don't run the development server with the port 80, which is the default
        for HTTP, you will need to add the port as well, e.g: mucenicu.rocks:8080 since it runs on
        that by default.
"""

# pylint: disable=wrong-import-position
# pylint: disable=invalid-name

__author__ = 'Marius Mucenicu <marius_mucenicu@yahoo.com>'

# Standard library
import ast
import os
import sys

# Third-party
import web

script_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(script_path)
sys.path.extend((root_path, script_path))

# Project specific
from mindgames import number_distance  # noqa

urls = (
    '/', 'Index',
    '/grade', 'Grade',
    '/play', 'Play',
    '/result', 'Result',
)

TEMPLATES_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TEMPLATES_PATH = '{0}/templates'.format(TEMPLATES_DIR)
render = web.template.render(TEMPLATES_PATH, base='layout')
app = web.application(urls, globals())


class Index:
    """
    Methods:
    ========
        GET()

    Miscellaneous objects:
    ======================
        Except the above, all other objects in this class are considered implementation details.
    """

    def GET(self):
        return render.index()


class Grade:
    """
    Methods:
    ========
        GET()

    Miscellaneous objects:
    ======================
        Except the above, all other objects in this class are considered implementation details.
    """

    def GET(self):
        return render.grade()


class Play:
    """
    Methods:
    ========
        POST()

    Miscellaneous objects:
    ======================
        Except the above, all other objects in this class are considered implementation details.
    """

    def POST(self):
        level = web.input().get('level')
        if not level:
            raise web.seeother('/grade')
        else:
            data = number_distance.play(level)
            if not data:
                raise web.internalerror('Oops. I fucked up! :D')
            else:
                return render.play(data)


class Result:
    """
    Methods:
    ========
        POST()

    Miscellaneous objects:
    ======================
        Except the above, all other objects in this class are considered implementation details.
    """

    def POST(self):
        data = ast.literal_eval(web.input().get('raw_data'))
        answer = web.input().get('answer')
        result = number_distance.generate_results(data, answer)
        level = data.get('left_bound'), data.get('right_bound')
        question = '{0}{start}, {stop}{1}'.format(data.get('left_glyph'), data.get('right_glyph'),
                                                  start=data.get('start'), stop=data.get('stop'))

        if result[1]:
            return render.result_success(level)
        else:
            return render.result_failure(level, question, answer, result[0])


if __name__ == '__main__':
    if not ('WEBPY_ENV' in os.environ and os.environ['WEBPY_ENV'] == 'test'):
        print('Starting development server at: ', end='')
        app.run()
    else:
        print('We are in test mode')
