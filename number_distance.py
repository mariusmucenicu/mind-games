import sys

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
        ('b. very easy+ (including negative numbers)', (-10**2 - 1, 10**2 - 1)),
        ('c. easy', (0, 10**3 - 1)),
        ('d. easy+ (including negative numbers)', (-10**3 - 1, 10**3 - 1)),
        ('e. normal', (0, 10**4 - 1)),
        ('f. normal+ (including negative numbers)', (-10**4 - 1, 10**4 - 1)),
        ('g. hard', (0, 10**5 - 1)),
        ('h. hard+ (including negative numbers)', (-10**5 - 1, 10**5 - 1)),
        ('i. very hard', (0, 10**6 - 1)),
        ('j. very hard+ (including negative numbers)', (-10**6 - 1, 10**6 - 1)),
        ('k. impossible', (0, 10**9 - 1)),
        ('l. impossible+ (including negative numbers)', (-10**9 - 1, 10**9 - 1)),
    )

    difficulty_levels = OrderedDict(dict_data)
    difficulty_values = difficulty_levels.values()

    for min_value, max_value in difficulty_values:
        assert type(min_value) == int and type(max_value) == int, 'values must be integers'
        assert min_value <= max_value, 'invalid values for game difficulty'

    assert len(set(difficulty_values)) == len(difficulty_values), 'duplicates found'

    difficulty_keys = difficulty_levels.keys()
    user_choices = [choice.split('.')[0].strip().lower() for choice in difficulty_keys]
    user_choices_values = [choice.split('.')[1].strip().lower() for choice in difficulty_keys]

    assert len(set(user_choices)) == len(user_choices), 'duplicates found'
    assert len(set(user_choices_values)) == len(user_choices_values), 'duplicates found'

    if representation:
        return user_choices, user_choices_values
    else:
        return list(difficulty_values)


def calculate_statistics(correct, wrong):
    """Computes the statistics based on the amount of items in categories correct and wrong"""

    assert all(type(obj) in (int, float) for obj in (correct, wrong)), 'ints or floats expected'

    total = correct + wrong
    correct_percentage = round(correct / total * 100, 2)
    wrong_percentage = round(100 - correct_percentage, 2)

    return total, correct_percentage, wrong_percentage


def generate_results(start_value, stop_value):
    """
    Generates two results based on a question formed from start_value and stop_value
    One is human based via standard input, and the other is CPU based via a computation.

    start_value: int, the number to marks the beginning of the interval
    stop_value: int, the number that marks the end of the interval
    """

    assert type(start_value) == int and type(stop_value) == int, 'invalid types for interval limits'
    assert start_value < stop_value, 'invalid interval limits'

    left_symbols, right_symbols = ('[', '('), (']', ')')
    start = randint(start_value, stop_value)
    stop = randint(start, stop_value)
    left_symbol = choice(left_symbols)
    right_symbol = choice(right_symbols)

    user_raw_input = input('How many natural numbers are between: '
                           '{0}{start}, {stop}{1} ? '.format(left_symbol, right_symbol,
                                                             start=start, stop=stop))
    user_result, cpu_result = None, None

    try:
        user_result = int(user_raw_input)
    except ValueError:
            print('{0} is not a number. Please enter a number'.format(user_raw_input))
    else:
        if left_symbol == '[' and right_symbol == ']':
            cpu_result = len(range(start, stop + 1))
        elif left_symbol == '(' and right_symbol == ')':
            cpu_result = len(range(start, stop - 1))
        else:
            cpu_result = len(range(start, stop))

    return user_result, cpu_result


def change_difficulty(avg_correct, avg_wrong, level, total_levels):
    """
    Increases or decreases the game difficulty from a range of difficulties based on
    the success rate computed from avg_correct and avg_wrong

    avg_correct: int, number of correct answers
    avg_wrong: int, number of wrong answers
    level: tuple, current difficulty level from a range of difficulty levels
    total_levels: tuple, a tuple of tuples representing different difficulty levels
    """

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
        if level + 1 < total_levels:
            level += 1
            cheerful_quote = choice(cheerful_messages)
            print('{0}\nYou have an average of {1}% correct answers. '
                  'Auto increasing difficulty\n'.format(cheerful_quote, avg_statistics))
        else:
            print('You are playing at the maximum level and going strong.\n'
                  'Please consider e-mailing marius_mucenicu@yahoo.com for extra levels\n')
    else:
        if level:
            level -= 1
            criticism_quote = choice(criticism_messages)
            print('{0}\nYou have an average of {1}% correct answers. '
                  'Auto decreasing difficulty\n'.format(criticism_quote, avg_statistics))
        else:
            print('You are playing at the lowest level and still doing dreadfully.\n'
                  'You are a bad abacist, please consider stepping up your game!\n')

    return level


def start_game(game_mode, game_difficulty, game_difficulties):
    """
    Main game engine, creates an environment based on the game mode and difficulty and interacts
    with the user via standard input. The results from the user (via the standard input) are then
    compared with the results of a machine and output is displayed.

    It also generates statistics based on the amount of correct/incorrect answers and
    changes game difficulties automatically if the game_mode is (you guessed it): 'auto'.

    game_mode: str, game mode selected by the user, possible values: 'auto' or 'manual'
    game_difficulty: tuple, game difficulty selected by the user,
    in the form of (min_value, max_value) where the values represent the interval limits
    game_difficulties: tuple of tuples, all levels available as game difficulties
    """

    assert game_mode in ('auto', 'manual'), 'invalid game mode'
    assert len(game_difficulty) == 2, 'invalid difficulty format'
    assert all(isinstance(val, int) for val in game_difficulty), 'invalid game difficulty'
    assert game_difficulty[0] <= game_difficulty[1], 'invalid game difficulty values'
    assert game_difficulty in game_difficulties, 'invalid input data'

    total_correct, total_wrong = 0, 0
    avg_correct, avg_wrong, mean = 0, 0, 0
    difficulty_levels = len(game_difficulties)
    difficulty_level = game_difficulties.index(game_difficulty)

    start_value = game_difficulty[0]
    stop_value = game_difficulty[1]

    while True:
        try:
            user_result, cpu_result = generate_results(start_value, stop_value)

            if user_result is None or cpu_result is None:
                continue

            if game_mode == 'auto':
                if user_result == cpu_result:
                    total_correct += 1
                    avg_correct += 1
                    print('Correct!\n')
                else:
                    total_wrong += 1
                    avg_wrong += 1
                    print('False\nYour result: {0}\nCorrect result: {1}\n'.format(user_result,
                                                                                  cpu_result))

                mean += 1

                if mean == 5:
                    difficulty_level = change_difficulty(avg_correct, avg_wrong,
                                                         difficulty_level, difficulty_levels)
                    start_value = game_difficulties[difficulty_level][0]
                    stop_value = game_difficulties[difficulty_level][1]
                    avg_correct, avg_wrong, mean = 0, 0, 0
            elif user_result == cpu_result:
                total_correct += 1
                print('Correct!\n')
            else:
                total_wrong += 1
                print('False\nYour result: {0}\nCorrect result: {1}\n'.format(user_result,
                                                                              cpu_result))

            if randint(1, 10) == 9:
                print('Remember this runs forever, you can always exit by hitting Ctrl-C on Windows'
                      ', or Ctrl-D on Unix\n')

        except KeyboardInterrupt:
            print('\nGracefully exiting. Have a good day, thank you for your time :)')
            total, correct, wrong = calculate_statistics(total_correct, total_wrong)
            print('Your summary for today: {0} correct ({1}%), '
                  '{2} wrong ({3}%) out of a total of {4}'.format(total_correct, correct,
                                                                  total_wrong, wrong, total))
            sys.exit(0)


def process_input(user_input):
    """
    Processes a raw input from the keyboard, validates it and returns a game mode and difficulty
    based on the selected option
    """

    assert user_input in ('a', 'b'), 'invalid choice'

    difficulties = fetch_difficulties(internal=True)
    user_choices, user_choices_values = fetch_difficulties(representation=True)
    difficulties_representation = [
        '{0}. {1}'.format(user_choices[num].upper(), user_choices_values[num].capitalize())
        for num in range(len(user_choices))
    ]

    if user_input == 'a':
        return 'auto', difficulties[0], difficulties  # for 'auto' we fetch the easiest difficulty
    else:
        manual_options = ''.join('\n\t{option}'.format(option=option)
                                 for option in difficulties_representation)
        manual_choice = input('\nChoose one of the following difficulty modes '
                              '(using the desired mode\'s letter):{0}\n'
                              'Please enter your option here -> '.format(manual_options)).lower()

        assert manual_choice in user_choices, 'invalid choice'

        difficulty_level = user_choices.index(manual_choice)
        return 'manual', difficulties[difficulty_level], difficulties


def explain_game():
    """Procedure which does a brief description of the game and its rules"""

    game_description = (
        '\nHello and welcome to the fascinating world of arithmetic\n'
        'This game aims to mimic the behavior of an abacus (without the beads that is)\n'
    )
    game_rules = (
        'The rules are pretty simple:\n'
        'You will be given a series of numeric intervals\n'
        'For each interval you have to type in how many numbers are in that interval\n'
        'The intervals are of many different types but that\'s a whole nother story.\n'
        '\nIn this version of the game you will be using the following types of intervals:'
        '\n\t* the open interval: For example, (0,9) has 8 numbers.'
        '\n\t* the closed interval: For example, [0,9] has 10 numbers.'
        '\n\t* the half-open interval: For example (0,9] has 9 numbers.\n'
    )
    print(game_description)
    print(game_rules)


def play():
    """The start procedure for the interactive counting game.

    Calls different procedures using procedural composition, based on different choices and results
    """

    explain_game()
    input_message = (
        'Please choose one of the following game modes (using the desired option\'s letter): '
        '\n\tA. Auto increase the difficulty based on your skill.'
        '\n\tB. Manually choose the difficulty.\nPlease enter your option here -> '
    )

    user_input = input(input_message).lower()
    game_mode, game_difficulty, game_difficulties = process_input(user_input)

    assert game_mode and game_difficulty and game_difficulties, 'cannot start game without all data'

    start_game(game_mode, game_difficulty, game_difficulties)


if __name__ == "__main__":
    play()
