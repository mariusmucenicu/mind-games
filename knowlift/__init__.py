"""
Store logic and configuration for the entire project.

Functions:
==========
    create_app: Create and configure a flask application.

Modules:
========
    db: Handle database related functionality.
    default_settings: Store project level default settings (quick-start development settings).
    lexicon: Handle building sentences from a given lexicon.
    models: Define entities (and their attributes) and relationships among entities.
    number_distance: Handle mathematical intervals scenarios.
    views: Handle HTTP requests.

Notes:
======
    This package is intended to bundle all of the core functionality of this application.
    The default configuration stored in default_settings.py is intended for development only and
        it's unsuitable for production. Check the module's docstring for more information.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

# Standard Library
from logging import config

# Third-party
import flask

# Project specific
from knowlift import db
from knowlift import views


def create_app(config_filename):
    """
    Configure, register, setup and return a Flask application.

    :param config_filename: A file which holds the configuration needed when the app starts up.
    :type config_filename: str
    :return: A flask object which implements a WSGI application and acts as the central object.
    :rtype: flask.app.Flask
    """
    app = flask.Flask(__name__)
    app.config.from_pyfile(config_filename)
    config.dictConfig(app.config['LOGGING_CONFIG'])

    db.init_db(app)

    app.add_url_rule('/', 'index', views.index)
    app.add_url_rule('/about', 'about', views.about)
    app.add_url_rule('/grade', 'grade', views.grade)
    app.add_url_rule('/ladder', 'ladder', views.ladder)
    app.add_url_rule('/legal', 'legal', views.legal)
    app.add_url_rule('/play', 'play', views.play, methods=['POST'])
    app.add_url_rule('/result', 'result', views.result, methods=['POST'])

    app.register_error_handler(404, views.page_not_found)
    app.register_error_handler(500, views.internal_server_error)

    app.teardown_appcontext(db.close_connection)
    return app
