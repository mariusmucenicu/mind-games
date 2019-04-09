"""
Store logic and configuration for the entire project.

Modules:
========
    db: Handle database related functionality.
    default_settings: Store project level default settings (quick-start development settings).
    lexicon: Handle building sentences from a given lexicon.
    number_distance: Handle mathematical intervals scenarios.
    views: Handle HTTP requests.

Notes:
======
    This package is intended to bundle all of the core functionality of this application.
    The default configuration stored in the default_settings module is intended for development
        only and it's unsuitable for production. Check the module's docstring for more information.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""
