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
import web

# Project specific
from mindgames import settings
from mindgames import urls

app = web.application(urls.URLS, globals())  # pylint: disable=invalid-name


def _notfound():
    """Return a custom 404 page."""
    return web.notfound(settings.base_render.custom404())


def _internalerror():
    """Return a custom 500 page."""
    return web.internalerror(settings.base_render.custom500())


app.notfound = _notfound
app.internalerror = _internalerror

if __name__ == '__main__':
    print('Starting development server at: ', end='')
    app.run()
