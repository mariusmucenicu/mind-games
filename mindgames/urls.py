"""
Map a URL to the view that handles it.

Constants
=========
URLS: Container for URL-View mappings. The pattern is ('url-path-pattern', handler-class).

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

from mindgames import views

URLS = (
    '/', views.Index,
    '/about', views.About,
    '/fundraising', views.FundRaising,
    '/grade', views.Grade,
    '/ladder', views.Ladder,
    '/legal', views.Legal,
    '/play', views.Play,
    '/result', views.Result,
)
