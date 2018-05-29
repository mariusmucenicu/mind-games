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


def __find_keys_in_generate_results(keys_collection):
    expected_values = (
        'cpu_internal', 'cpu_representation', 'answer_representation', 'outcome', 'left_glyph',
        'right_glyph', 'answer', 'game_level', 'start_representation', 'stop_representation',
        'start_internal', 'stop_internal',
    )
    for key in expected_values:
        yield key in keys_collection


def test_generate_results():
    interval_correct_1 = {
        'left_glyph': '(', 'right_glyph': ')', 'start_internal': 7, 'stop_internal': 41,
        'start_representation': '7', 'stop_representation': '41', 'answer': 33, 'game_level': 0
    }
    interval_correct_2 = {
        'left_glyph': '[', 'right_glyph': ')', 'start_internal': 7, 'stop_internal': 41,
        'start_representation': '7', 'stop_representation': '41', 'answer': 34, 'game_level': 0
    }
    interval_correct_3 = {
        'left_glyph': '[', 'right_glyph': ']', 'start_internal': 7, 'stop_internal': 41,
        'start_representation': '7', 'stop_representation': '41', 'answer': 35, 'game_level': 0
    }
    interval_correct_4 = {
        'left_glyph': '(', 'right_glyph': ')', 'start_internal': 200000000, 'game_level': 11,
        'stop_internal': 350000001, 'start_representation': '200 000 000', 'answer': 150000000,
        'stop_representation': '350 000 001',
    }
    interval_wrong_1 = {
        'left_glyph': '(', 'right_glyph': ')', 'start_internal': 7, 'stop_internal': 41,
        'start_representation': '7', 'stop_representation': '41', 'answer': 38, 'game_level': 0
    }
    interval_wrong_2 = {
        'left_glyph': '[', 'right_glyph': ']', 'start_internal': 41, 'stop_internal': 7,
        'start_representation': '7', 'stop_representation': '41', 'answer': 35, 'game_level': 0
    }
    interval_wrong_3 = {
        'left_glyph': '[', 'right_glyph': ']', 'start_internal': 41, 'stop_internal': 7,
        'start_representation': '41', 'stop_representation': '7', 'answer': 35, 'game_level': 0
    }
    invalid_glyphs = {
        'left_glyph': ('|', '{', '/', ']', ')'),
        'right_glyph': ('|', '}', '/', '[', '('),
    }

    # test invalid glyph values
    for glyph_internal, glyph_representation in invalid_glyphs.items():
        sample_correct_interval = interval_correct_1.copy()
        for glyph in glyph_representation:
            sample_correct_interval[glyph_internal] = glyph
            tools.assert_equals(number_distance.generate_results(sample_correct_interval), None)

    # test invalid missing keys
    for key in iter(interval_correct_1.keys()):
        sample_incorrect_interval = interval_correct_1.copy()
        sample_incorrect_interval.pop(key)
        tools.assert_equals(number_distance.generate_results(sample_incorrect_interval), None)

    generated_values_correct = number_distance.generate_results(interval_correct_1)
    generated_values_correct_2 = (number_distance.generate_results(interval_correct_2))
    generated_values_correct_3 = (number_distance.generate_results(interval_correct_3))
    generated_values_wrong = number_distance.generate_results(interval_wrong_1)
    generated_values_wrong_2 = (number_distance.generate_results(interval_wrong_2))
    generated_values_wrong_3 = (number_distance.generate_results(interval_wrong_3))
    generated_values_wrong_4 = (number_distance.generate_results(interval_correct_4))

    tools.assert_equals(all(__find_keys_in_generate_results(generated_values_correct)), True)
    tools.assert_equals(all(__find_keys_in_generate_results(generated_values_wrong)), True)

    tools.assert_equals(generated_values_correct['answer_representation'], '33')
    tools.assert_equals(generated_values_correct['cpu_representation'], '33')
    tools.assert_equals(generated_values_correct['cpu_internal'], 33)
    tools.assert_equals(generated_values_correct['outcome'], True)

    tools.assert_equals(generated_values_correct_2['answer_representation'], '34')
    tools.assert_equals(generated_values_correct_2['cpu_representation'], '34')
    tools.assert_equals(generated_values_correct_2['cpu_internal'], 34)
    tools.assert_equals(generated_values_correct_2['outcome'], True)

    tools.assert_equals(generated_values_correct_3['answer_representation'], '35')
    tools.assert_equals(generated_values_correct_3['cpu_representation'], '35')
    tools.assert_equals(generated_values_correct_3['cpu_internal'], 35)
    tools.assert_equals(generated_values_correct_3['outcome'], True)

    tools.assert_equals(generated_values_wrong['answer_representation'], '38')
    tools.assert_equals(generated_values_wrong['cpu_representation'], '33')
    tools.assert_equals(generated_values_wrong['cpu_internal'], 33)
    tools.assert_equals(generated_values_wrong['outcome'], False)

    tools.assert_equals(generated_values_wrong_4['answer_representation'], '150 000 000')
    tools.assert_equals(generated_values_wrong_4['cpu_representation'], '150 000 000')
    tools.assert_equals(generated_values_wrong_4['cpu_internal'], 150000000)
    tools.assert_equals(generated_values_wrong_4['outcome'], True)

    tools.assert_equals(generated_values_wrong_2, None)
    tools.assert_equals(generated_values_wrong_3, None)


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
