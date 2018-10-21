"""
Kick off the development server.

Intended for developing purposes (testing the game, adding features, debugging, etc.), rather than
actual serving files on the internet. Should you want to publish the game and have people interact
with it over the internet, you should try to serve files through nginx/apache or a real mature web
server.

Usage:
======
    python -m bin.webapp [port]

Notes:
======
    Run it from the root folder not from within bin.
    If you don't specify a port it will default to 8080.
    Create your own personal domain in a few easy steps:
        1. Add 127.0.0.1 <domain_name.extension> to your hosts file, e.g: mucenicu.rocks.
        2. Pop open Chrome/Mozilla Firefox/Opera/etc. punch the domain and enjoy the game.
        3. Run the script on default HTTP port 80, i.e python -m bin.webapp 80
        4. Careful, if you don't run the development server on port 80 you will need to add
            the port as well when requesting pages, i.e mucenicu.rocks:8080 (in the browser), since
            the server uses 8080 by default.
"""

__author__ = 'Marius Mucenicu <marius_mucenicu@yahoo.com>'

# Third-party
import logging
import web

# Project specific
from mindgames import settings
from mindgames import urls

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = web.application(urls.URLS, globals())


def _load_session():
    """Initialize a session object using a particular type of storage (DiskStore, DBStore, etc.)"""
    db = web.database(dbn='sqlite', db='mindgames.db')
    store = web.session.DBStore(db, 'sessions')
    initializer = {'correct_answers': 0, 'incorrect_answers': 0, 'total_answers': 0, 'average': 5}
    session = web.session.Session(app, store, initializer)
    web.config._session = session


def _internalerror():
    """Return a custom 500 page."""
    return web.internalerror(settings.base_render.custom_5xx())


def _notfound():
    """Return a custom 404 page."""
    return web.notfound(settings.base_render.custom_404())


app.notfound = _notfound
app.internalerror = _internalerror

if __name__ == '__main__':
    logger.info('Checking database status')
    settings.check_database()
    logger.info('Initializing session object')
    _load_session()
    logger.info('Starting development server')
    app.run()
