"""
Main package for all knowlift tests.

Modules:
========
    test_lexicon: Test knowlift.lexicon functionality.
    test_number_distance: Test knowlift.number_distance functionality.
    test_web: Test bin.webapp functionality.

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

# Standard library
import logging

# TODO(Marius): Remove the level argument once you drop support for Python 3.6
logging.disable(level=logging.CRITICAL)  # Keep the console clean during tests
