# Third-party
from nose import tools

# Project specific
from mindgames import number_distance


def test_fetch_difficulties():
    tools.assert_raises(AssertionError, number_distance.fetch_difficulties, True, True)
    tools.assert_raises(AssertionError, number_distance.fetch_difficulties, False, False)
    tools.assert_raises(AssertionError, number_distance.fetch_difficulties, 1, False)
    tools.assert_raises(AssertionError, number_distance.fetch_difficulties, 'truthy', False)
    tools.assert_raises(AssertionError, number_distance.fetch_difficulties, ['one'], False)
    tools.assert_raises(AssertionError, number_distance.fetch_difficulties, False, 0)
    tools.assert_raises(AssertionError, number_distance.fetch_difficulties, False, 'falsy')
    tools.assert_raises(AssertionError, number_distance.fetch_difficulties, True, '')

    available_choices = number_distance.fetch_difficulties(representation=True)
    internal_difficulties = set(number_distance.fetch_difficulties(internal=True))
    additive_inverses = set(pair for pair in internal_difficulties if pair[0] < 0)
    progressive_intervals = internal_difficulties - additive_inverses

    # representation values
    tools.assert_equals(len(set(available_choices)), len(available_choices))
    # internal values
    tools.assert_equals(
        all(negative + positive == 0 for negative, positive in additive_inverses),
        True
    )
    tools.assert_equals(
        all(lower_bound[0] == 0 for lower_bound in progressive_intervals),
        True
    )


def test_calculate_statistics():
    correct_p = round(3/23 * 100, 2)
    wrong_p = round(100 - correct_p, 2)
    tools.assert_equals(number_distance.calculate_statistics(3, 20), (23, correct_p, wrong_p))
    tools.assert_raises(AssertionError, number_distance.calculate_statistics, 3.0, 15)
    tools.assert_raises(AssertionError, number_distance.calculate_statistics, 3.0, 20.0)


def test_change_difficulty():
    sample_difficulties = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]

    tools.assert_equals(
        number_distance.change_difficulty(3, 20, [1, 2], sample_difficulties),
        [1, 2]
    )
    tools.assert_equals(
        number_distance.change_difficulty(3, 20, [3, 4], sample_difficulties),
        [1, 2]
    )
    tools.assert_equals(
        number_distance.change_difficulty(3, 20, [9, 10], sample_difficulties),
        [7, 8]
    )
    tools.assert_equals(
        number_distance.change_difficulty(10, 10, [9, 10], sample_difficulties),
        [9, 10]
    )
    tools.assert_equals(
        number_distance.change_difficulty(10, 10, [7, 8], sample_difficulties),
        [9, 10]
    )
    tools.assert_equals(
        number_distance.change_difficulty(10, 10, [1, 2], sample_difficulties),
        [3, 4]
    )
    tools.assert_raises(
        AssertionError,
        number_distance.change_difficulty, 10, 10, ['100', '100'], sample_difficulties
    )
    tools.assert_raises(
        AssertionError,
        number_distance.change_difficulty, 10, 10, [100, 100], sample_difficulties
    )
