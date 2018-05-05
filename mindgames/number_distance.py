"""
Implement the interface for a simple mathematical game based on intervals.

Functions:
==========
    calculate_statistics: Compute statistics based on amount of correct/wrong answers.
    change_game_level: Increment/decrement the degree of difficulty based on calculate_statistics().
    fetch_game_level: Return a game level from a series of game levels, based on user preference.
    generate_interval: Generate an interval which is a subset within the upper/lower bound limits.
    generate_results: Compare user results against the expected results for a given question.
    play: Entry point for the game.
    validate_game_levels: Ensure the game levels respect certain criteria.

CONSTANTS:
==========
    GAME_LEVELS: A series of available game levels ranging in difficulty.

Miscellaneous objects:
======================
    Except the above, all other objects in this module are to be considered implementation details.
"""

__author__ = 'Marius Mucenicu <marius_mucenicu@yahoo.com>'

# Standard library
import logging
import random

GAME_LEVELS = (
    (0, 10**2 - 1),
    (-10**2 + 1, 10**2 - 1),
    (0, 10**3 - 1),
    (-10**3 + 1, 10**3 - 1),
    (0, 10**4 - 1),
    (-10**4 + 1, 10**4 - 1),
    (0, 10**5 - 1),
    (-10**5 + 1, 10**5 - 1),
    (0, 10**6 - 1),
    (-10**6 + 1, 10**6 - 1),
    (0, 10**9 - 1),
    (-10**9 + 1, 10**9 - 1),
)


def calculate_statistics(correct, wrong):
    """
    Compute the statistics based on the total number of correct and wrong answers.

    Args:
        :param correct (int): Number of correct answers.
        :param wrong (int): Number of wrong answers.

    Returns:
        A tuple of length 3 of the form:
            (total number of answers, correct percentage (of total), wrong percentage (of total))
    """
    total = correct + wrong
    correct_percentage = round(correct / total * 100, 2)
    wrong_percentage = round(100 - correct_percentage, 2)
    return total, correct_percentage, wrong_percentage


def change_game_level(avg_correct, avg_wrong, game_level, all_game_levels):
    """
    Increase or decrease the game difficulty level from a range of levels based on the success rate.

    Args:
        :param avg_correct (int): Number of correct answers.
        :param avg_wrong (int): Number of wrong answers.
        :param game_level (tuple): Current game level.
        :param all_game_levels (tuple): Available game levels.

    Returns:
        A tuple of length 2 of the form:
            (lower_bound, upper_bound)
    """
    assert game_level in all_game_levels, 'invalid input data'

    GAME_LEVELS = len(all_game_levels)
    game_level = all_game_levels.index(game_level)

    cheerful_messages = (
        'Congratulations on your success! You have made us all proud. Keep up the good work!',
        "Keep being awesome, and I'll keep saying congratulations.",
        'I love to see good things come to good people. This is one of those times.',
        'I have so much pride in my heart right now. It might even be a sin.',
        'You are our shining star. Well done.',
        'Congratulations for scaling new heights and setting new standards.',
        "If Oscars were given for a job well done, I'd nominate you!"
        'Congratulations for your fantastic achievement!',
    )
    criticism_messages = (
        'Tell me… Is being stupid a profession or are you just gifted?',
        "Zombies eat brains. You're safe.",
        "I'd agree with you but then we'd both be wrong.",
        "I'll try being nicer, if you try being smarter.",
        "Well at least your mom thinks you're pretty…",
        'I thought I had seen the pinnacle of stupid… Then I met you.',
        "If had a dollar for every smart thing you say. I'll be poor.",
    )

    avg_statistics = calculate_statistics(avg_correct, avg_wrong)[1]

    if avg_statistics >= 50:
        if game_level + 1 < GAME_LEVELS:
            game_level += 1
            cheerful_quote = random.choice(cheerful_messages)
            print('{0}\nYou have an average of {1}% correct answers. '
                  'Auto increasing difficulty\n'.format(cheerful_quote, avg_statistics))
        else:
            print('You are playing at the maximum level and going strong.\n'
                  'Please consider e-mailing marius_mucenicu@yahoo.com for extra levels\n')
    else:
        if game_level:
            game_level -= 1
            criticism_quote = random.choice(criticism_messages)
            print('{0}\nYou have an average of {1}% correct answers. '
                  'Auto decreasing difficulty\n'.format(criticism_quote, avg_statistics))
        else:
            print('You are playing at the lowest level and still doing dreadfully.\n'
                  'You are a bad abacist, please consider stepping up your game!\n')
    return all_game_levels[game_level]


def fetch_game_level(user_input):
    """
    Fetch a particular game level based on a given input.

    Args:
        :param user_input (str): A cardinal number used to extract a game level from a tuple.

    Returns:
        A tuple of length 2 of the form:
            (lower_bound, upper_bound)
    """
    try:
        game_level = int(user_input.strip())
    except ValueError as e:
        logging.exception(e)
        return None

    if validate_game_levels(GAME_LEVELS) and 0 <= game_level < len(GAME_LEVELS):
        return GAME_LEVELS[game_level]
    else:
        logging.error('Unable to fetch the game level with index: {0}'.format(game_level))
        return None


def generate_interval(game_level):
    """
    Generate an interval within two limits.

    Args:
        :param game_level (tuple): Upper bound and lower bound values for an interval.

    Returns:
        A dictionary of length 2 comprising of:
            1. the 'raw data' used to create the mathematical interval (limits, glyphs).
            2. the formatted 'interval' based on data from step 1.
    """
    if game_level is None:
        return game_level
    else:
        start_value = game_level[0]
        stop_value = game_level[1]
        left_glyphs, right_glyphs = ('[', '('), (']', ')')
        start = random.randint(start_value, stop_value)
        stop = random.randint(start, stop_value)
        left_glyph = random.choice(left_glyphs)
        right_glyph = random.choice(right_glyphs)

        data = {
            'raw_data': {
                'left_glyph': left_glyph,
                'right_glyph': right_glyph,
                'start': start,
                'stop': stop,
                'game_level': GAME_LEVELS.index(game_level),
            },
            'interval': (
                '{0}{start}, {stop}{1}'.format(left_glyph, right_glyph, start=start, stop=stop)
            )
        }
        return data


def generate_results(data, value):
    """
    Compare a given value (usually from a user) against a computed value and return the results.

    Args:
        :param data (dict): A mathematical interval of a fixed length.
        :param value (int): A value used for indicating the total numbers in the given interval.

    Returns:
        A tuple of length 2 of the form:
            (cpu_result, human_result == cpu_result)
    """
    assert data, 'no data'
    assert value, 'invalid value'

    try:
        int(value)
    except ValueError:
        raise AssertionError('Invalid data received for value')

    left_glyph = data.get('left_glyph')
    right_glyph = data.get('right_glyph')
    start = data.get('start')
    stop = data.get('stop')
    cpu_result = None

    if left_glyph == '[' and right_glyph == ']':
        cpu_result = len(range(start, stop + 1))
    elif left_glyph == '(' and right_glyph == ')':
        cpu_result = len(range(start, stop - 1))
    else:
        cpu_result = len(range(start, stop))

    assert cpu_result is not None, 'correct data type and format received, invalid values'
    return cpu_result, cpu_result == int(value)


def play(user_input):
    """
    Start the game.

    Args:
        :param user_input (str): A value corresponding to a game level.

    Returns:
        See generate_interval's function for the return value.
    """
    game_level = fetch_game_level(user_input)
    return generate_interval(game_level)


def validate_game_levels(game_levels):
    """
    Validate a set of game levels against a set of rules.

    Args:
        :param game_levels (tuple): A series of game levels.

    Returns:
        A boolean object: True if all game levels are valid, False otherwise.

    Notes:
        Game levels should meet the following 2 criteria:
        1. Should be unique across the entire levels (not having a level appear multiple times).
        2. The game difficulties themselves should be valid mathematical intervals, i.e the lower
            bound should not be greater than the upper bound.
    """

    if not len(set(game_levels)) == len(game_levels):
        return False
    else:
        for lower_bound, upper_bound in game_levels:
            if lower_bound > upper_bound:
                return False
        else:
            return True
