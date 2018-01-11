from mindgames import number_distance as nd
from nose.tools import assert_equals, assert_raises


def test_fetch_difficulties():
    assert_raises(AssertionError, nd.fetch_difficulties, True, True)
    assert_raises(AssertionError, nd.fetch_difficulties, False, False)
    assert_raises(AssertionError, nd.fetch_difficulties, 1, False)
    assert_raises(AssertionError, nd.fetch_difficulties, 'truthy', False)
    assert_raises(AssertionError, nd.fetch_difficulties, ['one'], False)
    assert_raises(AssertionError, nd.fetch_difficulties, False, 0)
    assert_raises(AssertionError, nd.fetch_difficulties, False, 'falsy')
    assert_raises(AssertionError, nd.fetch_difficulties, True, '')

    user_choices, user_choices_values = nd.fetch_difficulties(representation=True)
    internal_difficulties = set(nd.fetch_difficulties(internal=True))
    additive_inverses = set(pair for pair in internal_difficulties if pair[0] < 0)
    progressive_intervals = internal_difficulties - additive_inverses

    # representation values
    assert_equals(len(set(user_choices)), len(user_choices))
    assert_equals(len(set(user_choices_values)), len(user_choices_values))
    # internal values
    assert_equals(all(negative + positive == 0 for negative, positive in additive_inverses), True)
    assert_equals(all(lower_bound[0] == 0 for lower_bound in progressive_intervals), True)


def test_calculate_statistics():
    correct_p = round(3/23 * 100, 2)
    wrong_p = round(100 - correct_p, 2)
    assert_equals(nd.calculate_statistics(3, 20), (23, correct_p, wrong_p))
    assert_raises(AssertionError, nd.calculate_statistics, 3.0, 15)
    assert_raises(AssertionError, nd.calculate_statistics, 3.0, 20.0)


def test_change_difficulty():
    sample_difficulties = [
        [1, 2],
        [3, 4],
        [5, 6],
        [7, 8],
        [9, 10]
    ]

    assert_equals(nd.change_difficulty(3, 20, [1, 2], sample_difficulties), [1, 2])
    assert_equals(nd.change_difficulty(3, 20, [3, 4], sample_difficulties), [1, 2])
    assert_equals(nd.change_difficulty(3, 20, [9, 10], sample_difficulties), [7, 8])
    assert_equals(nd.change_difficulty(10, 10, [9, 10], sample_difficulties), [9, 10])
    assert_equals(nd.change_difficulty(10, 10, [7, 8], sample_difficulties), [9, 10])
    assert_equals(nd.change_difficulty(10, 10, [1, 2], sample_difficulties), [3, 4])
    assert_raises(AssertionError, nd.change_difficulty, 10, 10, ['100', '100'], sample_difficulties)
    assert_raises(AssertionError, nd.change_difficulty, 10, 10, [100, 100], sample_difficulties)
