"""
Test mindgames.number_distance functionality.

Functions:
==========
    test_calculate_statistics: Test mindgames.number_distance.calculate_statistics functionality.
    test_change_game_level: Test mindgames.number_distance.change_game_level functionality.
    test_fetch_game_level: Test mindgames.number_distance.fetch_game_level functionality.
    test_generate_results: Test mindgames.number_distance.generate_results functionality.
    test_prettify_number: Test mindgames.number_distance.prettify_number functionality.

Miscellaneous objects:
======================
    Except the above, all other objects in this module are to be considered implementation details.
"""

# Third-party
from nose import tools

# Project specific
from mindgames import number_distance


def test_calculate_statistics():
    tools.assert_equals(number_distance.calculate_statistics(3, 20), (23, 13.04, 86.96))
    tools.assert_equals(number_distance.calculate_statistics(3, 20), (23.0, 13.04, 86.96))
    tools.assert_equals(number_distance.calculate_statistics(3.0, 15), (18.0, 16.67, 83.33))
    tools.assert_equals(number_distance.calculate_statistics(19, 20), (39, 48.72, 51.28))
    tools.assert_equals(number_distance.calculate_statistics(15.0, 20), (35.0, 42.86, 57.14))
    tools.assert_equals(number_distance.calculate_statistics(20.0, 20), (40.0, 50.0, 50.0))


def test_change_game_level():
    sample_difficulties = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]

    decrease_difficulty = 3, 20, [3, 4], sample_difficulties
    tools.assert_equals(number_distance.change_game_level(*decrease_difficulty), [1, 2])

    decrease_difficulty_2nd = 3, 20, [9, 10], sample_difficulties
    tools.assert_equals(number_distance.change_game_level(*decrease_difficulty_2nd), [7, 8])

    increase_difficulty = 10, 10, [7, 8], sample_difficulties
    tools.assert_equals(number_distance.change_game_level(*increase_difficulty), [9, 10])

    increase_difficulty_2nd = 10, 10, [1, 2], sample_difficulties
    tools.assert_equals(number_distance.change_game_level(*increase_difficulty_2nd), [3, 4])

    same_difficulty = 3, 20, [1, 2], sample_difficulties
    tools.assert_equals(number_distance.change_game_level(*same_difficulty), [1, 2])

    same_difficulty_2nd = 10, 10, [9, 10], sample_difficulties
    tools.assert_equals(number_distance.change_game_level(*same_difficulty_2nd), [9, 10])

    erroneus_data = 10, 10, ['100', '100'], sample_difficulties
    tools.assert_raises(AssertionError, number_distance.change_game_level, *erroneus_data)

    erroneus_data_2nd = 10, 10, [100, 100], sample_difficulties
    tools.assert_raises(AssertionError, number_distance.change_game_level, *erroneus_data_2nd)


def test_fetch_game_level():
    tools.assert_equals(number_distance.fetch_game_level('bogus'), None)
    tools.assert_equals(number_distance.fetch_game_level('3.14'), None)
    tools.assert_equals(number_distance.fetch_game_level('15'), None)
    tools.assert_equals(number_distance.fetch_game_level('12'), None)
    tools.assert_equals(number_distance.fetch_game_level('-1'), None)
    tools.assert_equals(number_distance.fetch_game_level('0'), number_distance.GAME_LEVELS[0])
    tools.assert_equals(number_distance.fetch_game_level('7'), number_distance.GAME_LEVELS[7])


def test_generate_results():
    open_interval = {'left_glyph': '(', 'right_glyph': ')', 'start': 7, 'stop': 41}
    half_open_interval = {'left_glyph': '[', 'right_glyph': ')', 'start': 7, 'stop': 41}
    closed_interval = {'left_glyph': '[', 'right_glyph': ']', 'start': 7, 'stop': 41}

    invalid_answer = 'a'
    tools.assert_equals(number_distance.generate_results(open_interval, invalid_answer), None)
    invalid_answer2 = 'l0'  # the character 'el'
    tools.assert_equals(number_distance.generate_results(open_interval, invalid_answer2), None)
    invalid_answer3 = '(11,)'
    tools.assert_equals(number_distance.generate_results(open_interval, invalid_answer3), None)
    invalid_answer4 = '[11]'
    tools.assert_equals(number_distance.generate_results(open_interval, invalid_answer4), None)

    tools.assert_equals(number_distance.generate_results(open_interval, 33), (33, True))
    tools.assert_equals(number_distance.generate_results(half_open_interval, 34), (34, True))
    tools.assert_equals(number_distance.generate_results(closed_interval, 35), (35, True))

    tools.assert_not_equals(number_distance.generate_results(open_interval, 33)[0], 100)
    tools.assert_not_equals(number_distance.generate_results(half_open_interval, 33)[0], 100)
    tools.assert_not_equals(number_distance.generate_results(closed_interval, 33)[0], 100)


def test_prettify_number():
    tools.assert_equals(number_distance.prettify_number(100), '100')
    tools.assert_equals(number_distance.prettify_number(1000), '1 000')
    tools.assert_equals(number_distance.prettify_number(-1000), '-1 000')
    tools.assert_equals(number_distance.prettify_number(10000), '10 000')
    tools.assert_equals(number_distance.prettify_number(-10000), '-10 000')
    tools.assert_equals(number_distance.prettify_number(100000), '100 000')
    tools.assert_equals(number_distance.prettify_number(-100000), '-100 000')
    tools.assert_equals(number_distance.prettify_number(1000000), '1 000 000')
    tools.assert_equals(number_distance.prettify_number(-1000000), '-1 000 000')
    tools.assert_equals(number_distance.prettify_number(10000000), '10 000 000')
    tools.assert_equals(number_distance.prettify_number(-10000000), '-10 000 000')
    tools.assert_equals(number_distance.prettify_number(100000000), '100 000 000')
    tools.assert_equals(number_distance.prettify_number(-100000000), '-100 000 000')
    tools.assert_equals(number_distance.prettify_number(1000000000), '1 000 000 000')
    tools.assert_equals(number_distance.prettify_number(-1000000000), '-1 000 000 000')
    tools.assert_equals(number_distance.prettify_number(10000000000), '10 000 000 000')
    tools.assert_equals(number_distance.prettify_number(-10000000000), '-10 000 000 000')
    tools.assert_equals(number_distance.prettify_number(100000000000), '100 000 000 000')
    tools.assert_equals(number_distance.prettify_number(-100000000000), '-100 000 000 000')
