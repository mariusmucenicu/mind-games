"""
Kick off the web application.

Global variables:
=================
    app: The Flask application. Acts as a central registry for views, URLs, templates, etc.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

__author__ = 'Marius Mucenicu <marius_mucenicu@yahoo.com>'

# Standard library
import logging

# Third-party
import flask

# Project specific
from knowlift import views

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = flask.Flask(__name__)

app.add_url_rule('/', 'index', views.index)
app.add_url_rule('/about', 'about', views.about)
app.add_url_rule('/funding', 'funding', views.funding)
app.add_url_rule('/grade', 'grade', views.grade)
app.add_url_rule('/ladder', 'ladder', views.ladder)
app.add_url_rule('/legal', 'legal', views.legal)
app.add_url_rule('/play', 'play', views.play, methods=['POST'])
app.add_url_rule('/result', 'result', views.result, methods=['POST'])

app.register_error_handler(404, views.page_not_found)
app.register_error_handler(500, views.internal_server_error)