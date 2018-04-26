"""
Implement the interface for a simple mathematical game based on intervals.

Functions:
==========
    calculate_statistics: Compute statistics based on amount of correct/wrong answers.
    change_difficulty: Increment/decrement game difficulty based on calculate_statistics().
    fetch_difficulties: Return available game difficulties (comprising of upper/lower bound limits).
    generate_interval: Generate an interval which is a subset within the upper/lower bound limits.
    generate_results: Compare user results against the expected results for a given question.
    play: Entry point for the game.
    process_input: Return a particular difficulty from fetch_difficulties() based on user choice.

Miscellaneous objects:
======================
    Except the above, all other objects in this module are to be considered implementation details.
"""

__author__ = 'Marius Mucenicu <marius_mucenicu@yahoo>'

# Standard library
import ast
import collections
import random


def fetch_difficulties(representation=False, internal=False):
    """Return the game difficulties as a list of ordered tuples, from easiest to most difficult."""
    assert all(isinstance(obj, bool) for obj in (representation, internal)), 'invalid input types'
    assert representation or internal, 'at least one input should be true'
    assert not (representation and internal), 'only one input should be true, not both'

    # FIXME(Marius): return just the internal values and associate with user choice from front-end.
    dict_data = (
        ('a. very easy', (0, 10**2 - 1)),
        ('b. very easy+ (including negative numbers)', (-10**2 + 1, 10**2 - 1)),
        ('c. easy', (0, 10**3 - 1)),
        ('d. easy+ (including negative numbers)', (-10**3 + 1, 10**3 - 1)),
        ('e. normal', (0, 10**4 - 1)),
        ('f. normal+ (including negative numbers)', (-10**4 + 1, 10**4 - 1)),
        ('g. hard', (0, 10**5 - 1)),
        ('h. hard+ (including negative numbers)', (-10**5 + 1, 10**5 - 1)),
        ('i. very hard', (0, 10**6 - 1)),
        ('j. very hard+ (including negative numbers)', (-10**6 + 1, 10**6 - 1)),
        ('k. impossible', (0, 10**9 - 1)),
        ('l. impossible+ (including negative numbers)', (-10**9 + 1, 10**9 - 1)),
    )

    difficulty_levels = collections.OrderedDict(dict_data)
    difficulty_values = difficulty_levels.values()

    for min_value, max_value in difficulty_values:
        assert type(min_value) == int and type(max_value) == int, 'values must be integers'
        assert min_value <= max_value, 'invalid values for game difficulty'
    assert len(set(difficulty_values)) == len(difficulty_values), 'duplicates found'

    difficulty_keys = difficulty_levels.keys()
    user_choices = [choice.split('.')[0].strip().lower() for choice in difficulty_keys]
    assert len(set(user_choices)) == len(user_choices), 'duplicates found'

    if representation:
        return user_choices
    else:
        return list(difficulty_values)


def calculate_statistics(correct, wrong):
    """
    Compute the statistics based on the numbers represented by correct and wrong.

    Args:
        :param correct (int): Number of correct answers.
        :param wrong (int): Number of wrong answers.

    Returns:
        A tuple of length 3 of the form:
            (total number of items, correct percentage of total, wrong percentage of total)
    """
    assert all(type(obj) == int for obj in (correct, wrong)), 'integers expected'

    total = correct + wrong
    correct_percentage = round(correct / total * 100, 2)
    wrong_percentage = round(100 - correct_percentage, 2)
    return total, correct_percentage, wrong_percentage


def change_difficulty(avg_correct, avg_wrong, game_difficulty, all_difficulties):
    """
    Increase or decrease the game difficulty from a range of difficulties based on the success rate.

    Args:
        :param avg_correct (int): Number of correct answers.
        :param avg_wrong (int): Number of wrong answers.
        :param game_difficulty (tuple): Current difficulty level.
        :param all_difficulties (tuple): A range of difficulty levels.

    Returns:
        A tuple of length 2 of the form:
            (lower_bound, upper_bound)
    """
    assert game_difficulty in all_difficulties, 'invalid input data'

    difficulty_levels = len(all_difficulties)
    difficulty_level = all_difficulties.index(game_difficulty)

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
        if difficulty_level + 1 < difficulty_levels:
            difficulty_level += 1
            cheerful_quote = random.choice(cheerful_messages)
            print('{0}\nYou have an average of {1}% correct answers. '
                  'Auto increasing difficulty\n'.format(cheerful_quote, avg_statistics))
        else:
            print('You are playing at the maximum level and going strong.\n'
                  'Please consider e-mailing marius_mucenicu@yahoo.com for extra levels\n')
    else:
        if difficulty_level:
            difficulty_level -= 1
            criticism_quote = random.choice(criticism_messages)
            print('{0}\nYou have an average of {1}% correct answers. '
                  'Auto decreasing difficulty\n'.format(criticism_quote, avg_statistics))
        else:
            print('You are playing at the lowest level and still doing dreadfully.\n'
                  'You are a bad abacist, please consider stepping up your game!\n')
    return all_difficulties[difficulty_level]


def generate_interval(game_difficulty):
    """
    Generate an interval within two limits.

    Args:
        :param game_difficulty (tuple): Upper bound and lower bound values for an interval.

    Returns:
        A dictionary of length 2 comprising of:
            1. the 'raw data' used to create the mathematical interval (limits, glyphs)
            2. the formatted 'interval' based on data from 1.
    """
    start_value = game_difficulty[0]
    stop_value = game_difficulty[1]
    left_glyphs, right_glyphs = ('[', '('), (']', ')')
    start = random.randint(start_value, stop_value)
    stop = random.randint(start, stop_value)
    left_glyph = random.choice(left_glyphs)
    right_glyph = random.choice(right_glyphs)

    data = {
        'raw_data': {
            'left_glyph': left_glyph,
            'right_glyph': right_glyph,
            'left_bound': start_value,
            'right_bound': stop_value,
            'start': start,
            'stop': stop,
        },
        'interval': '{0}{start}, {stop}{1}'.format(left_glyph, right_glyph, start=start, stop=stop)
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
    assert type(data) == dict, 'invalid data type, got {0}, expected dict'.format(type(data))
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


def process_input(user_input):
    """
    Fetch a game difficulty based on a given input.

    Args:
        :param user_input (str): A value corresponding to a game difficulty.

    Returns:
        A tuple of length 2 of the form:
            (lower_bound, upper_bound)
    """
    all_difficulties = fetch_difficulties(internal=True)
    available_choices = fetch_difficulties(representation=True)
    user_input = user_input.strip().lower()

    if len(user_input) > 1:
        user_input = ast.literal_eval(user_input)
        assert user_input in all_difficulties, 'invalid level'
        return user_input
    else:
        assert user_input in available_choices, 'invalid choice'
        difficulty_level = available_choices.index(user_input)
        return all_difficulties[difficulty_level]


def play(user_input):
    """
    Start the game.

    Args:
        :param user_input (str): A value corresponding to a game difficulty.

    Returns:
        See generate_interval's function for the return value.
    """
    game_difficulty = process_input(user_input)
    assert game_difficulty, 'cannot start game wihtout data'
    return generate_interval(game_difficulty)
