"""
Handle incoming requests.

Functions:
==========
    index: Get the homepage.
    internal_server_error: Get the custom internal server error page.
    about: Get the about page.
    funding: Get the funding page (this page contains credits to donors or supporters of any kind).
    grade: Get the grade page (this page contains all the difficulty levels).
    ladder: Get the ladder page.
    legal: Get the legal page (this page comprises legal information e.g GDPR, terms of use, etc).
    page_not_found: Get the custom not found page.
    play: Return a mathematical interval based on a particular difficulty level.
    result: Return a result based on the user's input.

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
import flask

# Project specific
from knowlift import number_distance

logger = logging.getLogger(__name__)


def index():
    return flask.render_template('index.html')


def about():
    return flask.render_template('about.html')


def funding():
    return flask.render_template('funding.html')


def grade():
    return flask.render_template('grade.html')


def ladder():
    return flask.render_template('ladder.html')


def legal():
    return flask.render_template('legal.html')


def page_not_found(e):
    return flask.render_template('404.html'), e.code


def internal_server_error(e):
    return flask.render_template('500.html'), e.code


def play():
    """
    Build a mathematical interval from a difficulty level. The difficulty level is represented by an
        integer which in turn is mapped to a tuple that contains the interval's limits.

    :return: A template containing either the interval in the form of a question or a custom error.
    :rtype: str
    """

    # TODO(Marius): raise the custom 500 instead of returning the template and log details about it.
    level = flask.request.form.get('level')
    data = number_distance.play(level)
    if not data:
        return flask.render_template('500.html')
    else:
        return flask.render_template('play.html', data=data)


def result():
    """
    Produce a result based on the user's input. Besides the user's answer, the input contains
        meta-data about the mathematical interval as well as the current game level. This is used
        both for validation purposes as well as for building further questions based on the same
        degree of difficulty.

    :return: A template containing either the appropriate result_data page or a custom error.
    :rtype: str
    """

    # TODO(Marius): raise the custom 500 instead of returning the template and log details about it.
    raw_data = flask.request.form.get('data')
    if not raw_data:
        data = {}
    else:
        data = json.loads(raw_data)

    result_data = number_distance.generate_result(data)
    if not result_data:
        return flask.render_template('500.html')
    elif result_data['outcome']:
        return flask.render_template('result_correct.html', data=result_data)
    else:
        return flask.render_template('result_incorrect.html', data=result_data)
