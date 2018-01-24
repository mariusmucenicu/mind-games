def check_ascii(raw_string):
    """Checks whether all the characters in an input string are ASCII compatible"""
    assert raw_string, 'invalid call with no data'
    assert type(raw_string) == str, 'invalid data type, str expected'

    return all(ord(letter) < 127 for letter in raw_string)


class Lexicon:
    def __init__(self, wordbook):
        """
        wordbook: dictionary, words representing the lexicon of a particular subject

        the wordbook must have the following form:
        {'part_of_speech' : {value1, value2, value3, etc.}}, i.e:

        {'subject': {'player', 'showman', 'etc'},
         'verb': {'go', 'run', 'etc'},
         'object': {'door', 'vault', 'etc'},
         'constituents': {'in', 'at', 'etc'}}
        """

        # class invariants
        assert wordbook, 'cannot operate on empty dictionary'
        assert isinstance(wordbook, dict), 'expected a dict type but got {0}'.format(type(wordbook))
        assert self.check_lexicon(wordbook), 'invalid lexicon'

        self.wordbook = wordbook

    def check_lexicon(self, wordbook):
        """Ensures the wordbook contains: unique lowercase words with just alphabetic characters"""
        # TODO(Marius): also check the parts of speech against the acknowledged classification
        assert all(type(term) == str and term.isalpha() and term.islower() and check_ascii(term)
                   for term in wordbook.keys()), 'invalid word type or format within keys'
        assert all(type(word_set) == set
                   for word_set in wordbook.values()), 'invalid data structure within values'

        checked_words = set()
        for word_set in wordbook.values():
            assert all(type(word) == str and word.isalpha() and word.islower() and check_ascii(word)
                       for word in word_set), 'invalid word found in {0}'.format(word_set)

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

        special_characters = {letter
                              for letter in raw_string
                              if not (letter.isalnum() or letter.isspace())}
        punctuation_marks = {'.', ',', '?', '!', '\'', '"', ':', ';', '-'}

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