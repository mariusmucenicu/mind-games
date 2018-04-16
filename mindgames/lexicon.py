__author__ = 'Marius Mucenicu <marius_mucenicu@yahoo.com>'


def check_ascii(raw_string):
    """Checks whether all the characters in an input string are ASCII compatible"""
    assert raw_string, 'invalid call with no data'
    assert type(raw_string) == str, 'invalid data type, str expected'
    return all(ord(letter) < 127 for letter in raw_string)


class ParserError(Exception):
    """Custom exception for dealing with invalid Sentence types"""
    pass


class Lexicon:
    def __init__(self, wordbook):
        """
        wordbook: dictionary, words representing the lexicon of a particular subject

        the wordbook must have the following form:
        {'part_of_speech' : {value1, value2, value3, etc.}}, i.e:

        {'subject': {'player', 'showman', 'etc'},
         'verb': {'go', 'run', 'etc'},
         'object': {'door', 'vault', 'etc'},
         'constituent': {'in', 'at', 'etc'}}
        """
        # class invariants
        assert wordbook, 'cannot operate on empty dictionary'
        assert isinstance(wordbook, dict), 'expected a dict type but got {0}'.format(type(wordbook))
        assert self.validate(wordbook), 'invalid lexicon'

        self.wordbook = wordbook

    def validate(self, wordbook):
        """Ensures the wordbook contains: unique lowercase words with just alphabetic characters"""
        # TODO(Marius): also check the parts of speech against the acknowledged classification
        assert len(wordbook) <= 64, 'too many parts of speech (word categories) in the lexicon'
        assert all(
            type(term) == str and term.isalpha() and term.islower() and check_ascii(term)
            for term in wordbook.keys()
        ), 'invalid word type or format within keys'
        assert all(
            type(word_set) == set
            for word_set in wordbook.values()
        ), 'invalid data structure within values'

        checked_words = set()
        for word_set in wordbook.values():
            assert word_set, 'empty data set not allowed'
            assert all(
                type(word) == str and word.isalpha() and word.islower() and check_ascii(word)
                for word in word_set
            ), 'invalid word found in {0}'.format(word_set)

            if word_set & checked_words:
                assert False, 'duplicate entries for words {0}'.format(word_set & checked_words)
            else:
                checked_words.update(word_set)
        return True

    def split_alnum(self, raw_string):
        """Parses a raw string and removes any non alphanumeric characters out of it.

        Words must be composed either entirely out of alphabetic characters: 'the', 'king', 'deuce'
        or entirely out of digits: '1990', but not mixed: 'th3', 'k1ng'

        returns: a list of formatted words (lowercase, special characters removed) and/or numbers
        """
        assert type(raw_string) == str, 'invalid data type, str expected'
        assert len(raw_string) <= 512, 'maximum input length of 512 characters exceeded'

        special_characters = {
            letter
            for letter in raw_string
            if not (letter.isalnum() or letter.isspace())
        }
        punctuation_marks = {'.', ',', '?', '!', "'", '"', ':', ';', '-'}

        for character in special_characters:
            if character not in punctuation_marks:
                raw_string = raw_string.replace(character, '')
            else:
                raw_string = raw_string.replace(character, ' ')

        words = raw_string.lower().split()
        assert all(word.isalpha() or word.isdigit() for word in words), 'alphanumeric words found'
        return words

    def scan_text(self, raw_string):
        """Scans a text and matches words against a lexicon to identify each word's class"""
        assert raw_string, 'invalid call with no data'
        assert check_ascii(raw_string), 'invalid characters'

        processed_words = []
        words = self.split_alnum(raw_string)

        for word in words:
            processed = False
            for key, value in self.wordbook.items():
                if word in value:
                    processed_words.append((key, word))
                    processed = True
            if not processed:
                processed_words.append(('error', word))
        return processed_words


class Sentence:
    def __init__(self, word_order):
        """
        word_order: string, represents the rule upon which sentences will built

        The most popular, acknowledged word orders are:
            * Subject Verb Object (SVO),
            * Subject Object Verb (SOV),
            * Verb Subject Object (VSO),
        All together they account for more than 85% of the world's languages
        """
        # class invariants
        assert type(word_order) == str, 'invalid input type, str expected'
        word_order = word_order.strip().lower()
        assert word_order in ('svo', 'sov', 'vso'), 'invalid word order'

        word_pattern = {
            'svo': ('subject', 'verb', 'object'),
            'sov': ('subject', 'object', 'verb'),
            'vso': ('verb', 'subject', 'object'),
        }
        self.expected_order = word_pattern[word_order]

    def build(self, words):
        """Builds a simple sentence (one independent clause) based on the word order

        words: list, contains 2 item tuples of the form ('token', 'word'), i.e ('verb', 'build')
        """
        assert words, 'invalid call with no data'
        assert all(
            len(pair) == 2 and type(pair) == tuple
            for pair in words
        ), 'invalid (token, word) data structure or items within != str'
        assert all(
            type(item) == str
            for pair in words
            for item in pair
        ), 'invalid element type in token-word pair'

        position = 0
        sentence = []

        for token, word in words:
            if token == 'constituent':
                continue
            elif token == self.expected_order[position]:
                sentence.append(word)
                if position + 1 >= len(self.expected_order):
                    return ' '.join(sentence)
                else:
                    position += 1
            else:
                raise ParserError(
                    'Expected {0} but got {1}'.format(self.expected_order[position], token)
                )
