from ast import literal_eval
from collections import OrderedDict
from random import choice, randint


def fetch_difficulties(representation=False, internal=False):
    """
    Returns either a tuple of two lists containing strings which are the available game difficulties
    or a list of tuples representing the game difficulties as internal values for the script
    """

    assert all(isinstance(obj, bool) for obj in (representation, internal)), 'invalid input types'
    assert representation or internal, 'at least one input should be true'
    assert not (representation and internal), 'only one input should be true, not both'

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

    difficulty_levels = OrderedDict(dict_data)
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
    """Computes the statistics based on the amount of items in categories correct and wrong"""

    assert all(type(obj) == int for obj in (correct, wrong)), 'integers expected'

    total = correct + wrong
    correct_percentage = round(correct / total * 100, 2)
    wrong_percentage = round(100 - correct_percentage, 2)
    return total, correct_percentage, wrong_percentage


def change_difficulty(avg_correct, avg_wrong, game_difficulty, all_difficulties):
    """
    Increases or decreases the game difficulty from a range of difficulties based on
    the success rate computed from avg_correct and avg_wrong

    avg_correct: int, number of correct answers
    avg_wrong: int, number of wrong answers
    game_difficulty: tuple, current difficulty level from a range of game difficulties
    all_difficulties: tuple, a range of difficulty levels
    """

    assert game_difficulty in all_difficulties, 'invalid input data'

    difficulty_levels = len(all_difficulties)
    difficulty_level = all_difficulties.index(game_difficulty)

    cheerful_messages = (
        'Congratulations on your success! You have made us all proud. Keep up the good work!',
        'Keep being awesome, and I’ll keep saying congratulations.',
        'I love to see good things come to good people. This is one of those times.',
        'I have so much pride in my heart right now. It might even be a sin.',
        'You are our shining star. Well done.',
        'Congratulations for scaling new heights and setting new standards.',
        'If Oscars were given for a job well done, I’d nominate you! '
        'Congratulations for your fantastic achievement!',
    )
    criticism_messages = (
        'Tell me… Is being stupid a profession or are you just gifted?',
        'Zombies eat brains. You’re safe.',
        'I’d agree with you but then we’d both be wrong.',
        'I’ll try being nicer, if you try being smarter.',
        'Well at least your mom thinks you’re pretty…',
        'I thought I had seen the pinnacle of stupid… Then I met you.',
        'If had a dollar for every smart thing you say. I’ll be poor.',
    )

    avg_statistics = calculate_statistics(avg_correct, avg_wrong)[1]

    if avg_statistics >= 50:
        if difficulty_level + 1 < difficulty_levels:
            difficulty_level += 1
            cheerful_quote = choice(cheerful_messages)
            print('{0}\nYou have an average of {1}% correct answers. '
                  'Auto increasing difficulty\n'.format(cheerful_quote, avg_statistics))
        else:
            print('You are playing at the maximum level and going strong.\n'
                  'Please consider e-mailing marius_mucenicu@yahoo.com for extra levels\n')
    else:
        if difficulty_level:
            difficulty_level -= 1
            criticism_quote = choice(criticism_messages)
            print('{0}\nYou have an average of {1}% correct answers. '
                  'Auto decreasing difficulty\n'.format(criticism_quote, avg_statistics))
        else:
            print('You are playing at the lowest level and still doing dreadfully.\n'
                  'You are a bad abacist, please consider stepping up your game!\n')

    return all_difficulties[difficulty_level]


def generate_interval(game_difficulty):
    """Function description"""

    start_value = game_difficulty[0]
    stop_value = game_difficulty[1]

    left_glyphs, right_glyphs = ('[', '('), (']', ')')
    start = randint(start_value, stop_value)
    stop = randint(start, stop_value)
    left_glyph = choice(left_glyphs)
    right_glyph = choice(right_glyphs)

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
    """Function description"""
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
    """Function description"""
    all_difficulties = fetch_difficulties(internal=True)
    available_choices = fetch_difficulties(representation=True)
    user_input = user_input.strip().lower()

    if len(user_input) > 1:
        user_input = literal_eval(user_input)
        assert user_input in all_difficulties, 'invalid level'
        return user_input
    else:
        assert user_input in available_choices, 'invalid choice'
        difficulty_level = available_choices.index(user_input)
        return all_difficulties[difficulty_level]


def play(user_input):
    """Function description"""
    game_difficulty = process_input(user_input)
    assert game_difficulty, 'cannot start game wihtout data'
    return generate_interval(game_difficulty)
