"""
Test knowlift.lexicon functionality.

Classes:
========
    LexiconTest: Test the functionality under knowlift.lexion

Miscellaneous objects:
======================
    Except for the public objects exported by this module and their public APIs (if applicable),
        everything else is an implementation detail, and shouldn't be relied upon as it may change
        over time.
"""

# Standard library
import unittest

# Project specific
from knowlift import lexicon


def make_string(tokens, number):
    """Create a string from a sequence of tokens and a number."""
    word = ''
    for digit in str(number):
        word += tokens[int(digit)]
    return word


class LexiconTest(unittest.TestCase):

    def setUp(self):
        self.sample_wordbook = {
            'subject': {'i', 'player', 'julia', 'zuck'},
            'verb': {'run', 'go', 'start', 'swipe', 'push', 'acquiescence'},
            'object': {'bear', 'python', 'game', 'door'},
            'constituent': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that'}
        }
        self.detailed_wordbook = {
            'subject': {'i'},
            'verb': {'remember', 'used', 'was', 'were', 'spar', 'serve', 'walked', 'waddle'},
            'object': {'drinks', 'joint', 'bar', 'spot', 'robots', 'duck', 'lemonade', 'stand'},
            'constituent': {'to', 'at', 'this', 'but', 'no', 'it', 'a', 'where', 'up', 'then'},
        }
        self.sample_lexicon = lexicon.Lexicon(self.sample_wordbook)
        self.detailed_lexicon = lexicon.Lexicon(self.detailed_wordbook)

    def test_check_ascii(self):
        self.assertTrue(lexicon.check_ascii({'a': 'test'}))  # false positive
        self.assertTrue(all(lexicon.check_ascii(chr(x)) for x in range(0, 127)))
        self.assertFalse(any(lexicon.check_ascii(chr(x)) for x in range(127, 255)))
        self.assertRaises(TypeError, lexicon.check_ascii, [1, 2])
        self.assertRaises(TypeError, lexicon.check_ascii, ['abc'])
        self.assertRaises(TypeError, lexicon.check_ascii, 1234)

    def test_split_alphanum(self):
        self.assertRaises(
            AssertionError, self.sample_lexicon.split_alphanum, ' We the best music!!1one  '
        )
        self.assertRaises(
            AssertionError, self.sample_lexicon.split_alphanum, 'We234 t2h1e best mu$sic'
        )
        self.assertRaises(
            AssertionError, self.sample_lexicon.split_alphanum, 'd0ll4r$     multiple   s9 '
        )
        self.assertEqual(
            self.sample_lexicon.split_alphanum('    1234567890%$#%!@!^&*'),
            ['1234567890']
        )
        self.assertEqual(
            self.sample_lexicon.split_alphanum('    We the best music!!!one'),
            ['we', 'the', 'best', 'music', 'one']
        )
        self.assertEqual(
            self.sample_lexicon.split_alphanum('Slap,the,bear   !@#steal honey'),
            ['slap', 'the', 'bear', 'steal', 'honey']
        )
        self.assertEqual(
            self.sample_lexicon.split_alphanum('Pun,ch,the,  bear  steal honey'),
            ['pun', 'ch', 'the', 'bear', 'steal', 'honey']
        )
        self.assertEqual(
            self.sample_lexicon.split_alphanum('Pl,ay th,e num,ber game.'),
            ['pl', 'ay', 'th', 'e', 'num', 'ber', 'game']
        )
        self.assertEqual(
            self.sample_lexicon.split_alphanum('Slap,punch  shout at y"all!'),
            ['slap', 'punch', 'shout', 'at', 'y', 'all']
        )
        self.assertEqual(
            self.sample_lexicon.split_alphanum('Play,the,number,game!'),
            ['play', 'the', 'number', 'game']
        )
        self.assertEqual(
            self.sample_lexicon.split_alphanum('Play,the,num,be,r,game,!'),
            ['play', 'the', 'num', 'be', 'r', 'game']
        )
        self.assertEqual(
            self.sample_lexicon.split_alphanum('PlAy,ThE,NUM,be,R,game,!'),
            ['play', 'the', 'num', 'be', 'r', 'game']
        )
        self.assertEqual(
            self.sample_lexicon.split_alphanum('A, B, C'),
            ['a', 'b', 'c']
        )

    def test_valid_lexicon(self):
        valid_lexicon_bogus_values = {
            'subject': {*(rev[::-1] for rev in {'i', 'player', 'julia', 'zuck'})},
            'verb': {*(rev[::-1] for rev in {'run', 'go', 'start', 'push', 'acquiescence'})},
            'object': {*(rev[::-1] for rev in {'bear', 'python', 'game', 'door'})},
            'constituent': {*(rev[::-1] for rev in {'at', 'or', 'in', 'through', 'over', 'this'})}
        }
        valid_lexicon_bogus_keys = {
            'tcejbus': {*(rev[::-1] for rev in {'i', 'player', 'julia', 'zuck'})},
            'brev': {*(rev[::-1] for rev in {'run', 'go', 'start', 'push', 'acquiescence'})},
            'tcejbo': {*(rev[::-1] for rev in {'bear', 'python', 'game', 'door'})},
            'tneutitsnoc': {*(rev[::-1] for rev in {'at', 'or', 'in', 'through', 'over', 'this'})}
        }
        self.assertTrue(self.sample_lexicon.validate(valid_lexicon_bogus_values))
        self.assertTrue(self.sample_lexicon.validate(valid_lexicon_bogus_keys))

    def test_invalid_lexicon_data(self):
        """Test only strings which contain alphabetic characters are allowed."""
        invalid_entries = {
            'subject': {'i', 1, 'julia', 2},
            'verb': {'i', 'player', ('julia', 'moore'), ('zuck', 'mark')},
            'object': {'i', 'player', 'julia', 'zuck', 'z00m', 'm00re'},
            'constituent': {'i', 'player#', 'julia', 'zuck'},
            'adverb': {'i', 'player one', 'julia roberts', 'zuck mark'},
        }
        for entry in invalid_entries:
            invalid_lexicon = self.sample_wordbook.copy()
            invalid_lexicon[entry] = invalid_entries[entry]
            self.assertRaises(
                (AssertionError, AttributeError), self.sample_lexicon.validate, invalid_lexicon
            )

    def test_invalid_lexicon_case(self):
        invalid_lexicon_uppercase = {
            'subject': {'I', 'PLAYER', 'JULIA', 'ZUCK'},
            'verb': {'RUN', 'GO', 'START', 'SWIPE', 'PUSH', 'ACQUIESENCE'},
            'object': {'BEAR', 'PYTHON', 'GAME', 'DOOR'},
            'constituent': {'AT', 'OR', 'IN', 'THROUGH', 'OVER', 'THIS', 'THE', 'THAT'}
        }
        invalid_lexicon_mixcase = {
            'subject': {'I', 'PlAyEr', 'JuLiA', 'ZuCk'},
            'verb': {'RuN', 'Go', 'StArT', 'SwIpE', 'PuSh', 'AcQuIeSeNcE'},
            'object': {'BeAr', 'PyThOn', 'GaMe', 'DoOr'},
            'constituent': {'aT', 'oR', 'iN', 'THROugh', 'ovER', 'tHIs', 'tHE', 'thAT'}
        }
        self.assertRaises(AssertionError, self.sample_lexicon.validate, invalid_lexicon_uppercase)
        self.assertRaises(AssertionError, self.sample_lexicon.validate, invalid_lexicon_mixcase)

    def test_invalid_lexicon_duplicates(self):
        duplicate_entries = {
            'object': {'bear', 'python', 'game', 'door', 'zuck', 'julia', 'acquiescence'},
            'constituent': {'at', 'or', 'in', 'through', 'game', 'that', 'go', 'zuck'}
        }
        for entry in duplicate_entries:
            invalid_lexicon = self.sample_wordbook.copy()
            invalid_lexicon[entry] = duplicate_entries[entry]
            self.assertRaises(AssertionError, self.sample_lexicon.validate, invalid_lexicon)

    def test_invalid_lexicon_keys(self):
        invalid_entries = {
            'sub ject': {'i', 'player', 'julia', 'zuck'},
            'verb1': {'run', 'go', 'start', 'swipe', 'push', 'acquiescence'},
            'OBJECT': {'bear', 'python', 'game', 'door'},
            'CoNsTiTuEnT': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that'},
            'con$tituent': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that'}
        }
        for entry in invalid_entries:
            invalid_lexicon = self.sample_wordbook.copy()
            invalid_lexicon[entry] = invalid_entries[entry]
            self.assertRaises(AssertionError, self.sample_lexicon.validate, invalid_lexicon)

    def test_invalid_lexicon_nonascii(self):
        invalid_nonascii_keys = {
            'subject' + 'çèêëìíîïðñ': {'i', 'player', 'julia', 'zuck'},
            'verb': {'run', 'go', 'start', 'swipe', 'push', 'acquiescence'},
            'object': {'bear', 'python', 'game', 'door'},
            'constituent': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that'}
        }
        invalid_nonascii_values = {
            'subject': {'i', 'playèêër', 'juliìíîïa', 'zuçk'},
            'verb': {'run', 'gð', 'start', 'swipe', 'push', 'acquiesceñce'},
            'object': {'bear', 'python', 'game', 'door'},
            'constituent': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that'}
        }
        self.assertRaises(AssertionError, self.sample_lexicon.validate, invalid_nonascii_keys)
        self.assertRaises(AssertionError, self.sample_lexicon.validate, invalid_nonascii_values)

    def test_lexicon_max_keys(self):
        words = [chr(x) for x in range(97, 123)]
        valid_number_keys32 = {
            make_string(words, number): {make_string(words, number)}
            for number in range(32)
        }
        invalid_number_keys65 = {
            make_string(words, number): {make_string(words, number)}
            for number in range(65)
        }
        self.assertTrue(self.sample_lexicon.validate(valid_number_keys32))
        self.assertRaises(AssertionError, self.sample_lexicon.validate, invalid_number_keys65)

    def test_scan_text(self):
        robot_bar_fight = (
            'I remember I used to serve drinks at this local joint\n'
            'Cause I was broke but my focal point was\n'
            'This was no regular bar\n'
            'It was a spot where robots were ready to spar\n'
        )
        robot_parts_of_speech = [
            ('subject', 'i'), ('verb', 'remember'), ('subject', 'i'), ('verb', 'used'),
            ('constituent', 'to'), ('verb', 'serve'), ('object', 'drinks'),
            ('constituent', 'at'), ('constituent', 'this'), ('error', 'local'),
            ('object', 'joint'), ('error', 'cause'), ('subject', 'i'), ('verb', 'was'),
            ('error', 'broke'), ('constituent', 'but'), ('error', 'my'), ('error', 'focal'),
            ('error', 'point'), ('verb', 'was'), ('constituent', 'this'), ('verb', 'was'),
            ('constituent', 'no'), ('error', 'regular'), ('object', 'bar'),
            ('constituent', 'it'), ('verb', 'was'), ('constituent', 'a'), ('object', 'spot'),
            ('constituent', 'where'), ('object', 'robots'), ('verb', 'were'),
            ('error', 'ready'), ('constituent', 'to'), ('verb', 'spar')
        ]
        self.assertEqual(self.detailed_lexicon.scan_text(robot_bar_fight), robot_parts_of_speech)

    def test_scan_text_case(self):
        duck_upper_case = 'A DUCK WALKED UP TO A LEMONADE STAND'
        duck_mixed_case = (
            'ThEn hE WaDDlEd aWaY. '
            "(Waddle) (WAddLe) 'Til THE vErY NeXt day."
            '(Bum bum BUM bum ba-bada-DUM)'
        )
        duck_upper_parts_of_speech = [
            ('constituent', 'a'), ('object', 'duck'), ('verb', 'walked'), ('constituent', 'up'),
            ('constituent', 'to'), ('constituent', 'a'), ('object', 'lemonade'),
            ('object', 'stand')
        ]
        duck_mixed_parts_of_speech = [
            ('constituent', 'then'), ('error', 'he'), ('error', 'waddled'), ('error', 'away'),
            ('verb', 'waddle'), ('verb', 'waddle'), ('error', 'til'), ('error', 'the'),
            ('error', 'very'), ('error', 'next'), ('error', 'day'), ('error', 'bum'),
            ('error', 'bum'), ('error', 'bum'), ('error', 'bum'), ('error', 'ba'),
            ('error', 'bada'), ('error', 'dum')
        ]
        self.assertEqual(
            self.detailed_lexicon.scan_text(duck_upper_case), duck_upper_parts_of_speech
        )
        self.assertEqual(
            self.detailed_lexicon.scan_text(duck_mixed_case), duck_mixed_parts_of_speech
        )

    def test_scan_text_symbols_and_numbers(self):
        duck_punctuation_characters = (
            'Come.on.duck,lets,walk!to!the.store.'
            'Ill...buy-you-some-grapes.'
            'So;you;wont;have:to:ask::anymore.'
        )
        duck_mixed_characters = (
            'And::the,man,bought.SOME#,grapes##.'
            'He::gave,one,to.the##-duck-and-the-duck said:'
            'Hmmm..No thanks!!!!!$But$ you$ know$ what$ sounds$ ??good?'
        )
        duck_symbol_characters = (
            'H@e#y$! (b%u^m b&u*m b=u|m) G{o}t >a>n<y g`r~ap+es?',
            '$Hey$!!! (#$bum$# **bum** #bum#) {{Got}} any ``grapes``?',
            'Should-1990#-not.be.an::error!',
            'NUMBERS ARE ALLOWED, THE 6 OUT OF 49 ARE 24 3 21 12 8 4',
            duck_punctuation_characters,
            duck_mixed_characters,
        )
        duck_parts_of_speech = (
            [
                ('error', 'hey'), ('error', 'bum'), ('error', 'bum'), ('error', 'bum'),
                ('error', 'got'), ('error', 'any'), ('error', 'grapes')
            ],
            [
                ('error', 'hey'), ('error', 'bum'), ('error', 'bum'), ('error', 'bum'),
                ('error', 'got'), ('error', 'any'), ('error', 'grapes')
            ],
            [
                ('error', 'should'), ('error', '1990'), ('error', 'not'), ('error', 'be'),
                ('error', 'an'), ('error', 'error')
            ],
            [
                ('error', 'numbers'), ('error', 'are'), ('error', 'allowed'),
                ('error', 'the'), ('error', '6'), ('error', 'out'), ('error', 'of'),
                ('error', '49'), ('error', 'are'), ('error', '24'), ('error', '3'), ('error', '21'),
                ('error', '12'), ('error', '8'), ('error', '4')
            ],
            [
                ('error', 'come'), ('error', 'on'), ('object', 'duck'), ('error', 'lets'),
                ('error', 'walk'), ('constituent', 'to'), ('error', 'the'), ('error', 'store'),
                ('error', 'ill'), ('error', 'buy'), ('error', 'you'), ('error', 'some'),
                ('error', 'grapes'), ('error', 'so'), ('error', 'you'), ('error', 'wont'),
                ('error', 'have'), ('constituent', 'to'), ('error', 'ask'), ('error', 'anymore')
            ],
            [
                ('error', 'and'), ('error', 'the'), ('error', 'man'), ('error', 'bought'),
                ('error', 'some'), ('error', 'grapes'), ('error', 'he'), ('error', 'gave'),
                ('error', 'one'), ('constituent', 'to'), ('error', 'the'), ('object', 'duck'),
                ('error', 'and'), ('error', 'the'), ('object', 'duck'), ('error', 'said'),
                ('error', 'hmmm'), ('constituent', 'no'), ('error', 'thanks'),
                ('constituent', 'but'), ('error', 'you'), ('error', 'know'), ('error', 'what'),
                ('error', 'sounds'), ('error', 'good')
            ]
        )
        for position, text in enumerate(duck_symbol_characters):
            self.assertEqual(self.detailed_lexicon.scan_text(text), duck_parts_of_speech[position])

    def test_scan_simple_and_compound_sentences(self):
        self.detailed_lexicon.wordbook = {
            'verb': {'spar', 'punch', 'wrestle', 'smack', 'open', 'go'},
            'object': {'bear', 'door'},
            'constituent': {'in', 'the'},
        }
        sentences = (
            'Punch the bear',
            'Punch the bear in the face',
            'Open the door',
            'Go through the door',
            'Open the door and smack the bear in the nose and then...wrestle it!'
        )
        parts_of_speech = (
            [
                ('verb', 'punch'), ('constituent', 'the'), ('object', 'bear')
            ],
            [
                ('verb', 'punch'), ('constituent', 'the'), ('object', 'bear'),
                ('constituent', 'in'), ('constituent', 'the'), ('error', 'face')
            ],
            [
                ('verb', 'open'), ('constituent', 'the'), ('object', 'door')
            ],
            [
                ('verb', 'go'), ('error', 'through'), ('constituent', 'the'), ('object', 'door')
            ],
            [
                ('verb', 'open'), ('constituent', 'the'), ('object', 'door'), ('error', 'and'),
                ('verb', 'smack'), ('constituent', 'the'), ('object', 'bear'),
                ('constituent', 'in'), ('constituent', 'the'), ('error', 'nose'), ('error', 'and'),
                ('error', 'then'), ('verb', 'wrestle'), ('error', 'it')
            ]
        )
        for position, sentence in enumerate(sentences):
            self.assertEqual(self.detailed_lexicon.scan_text(sentence), parts_of_speech[position])

    def test_scan_text_exceptions(self):
        self.assertRaises(
            AssertionError, self.sample_lexicon.scan_text, '0n3, tw0, thr33'
        )
        self.assertRaises(
            AssertionError, self.sample_lexicon.scan_text, '0n#3, t$w$0, thr**33'
        )
        self.assertRaises(
            AssertionError, self.sample_lexicon.scan_text, '“Come on duck, let’s walk..”'
        )
        self.assertRaises(
            AssertionError, self.sample_lexicon.scan_text, chr(255) + chr(254)
        )


class SentenceTest(unittest.TestCase):

    def setUp(self):
        sample_lexicon = {
            'subject': {'player'},
            'verb': {'smack', 'punch', 'go', 'open'},
            'object': {'bear', 'door', 'face', 'nose'},
            'constituent': {'in', 'the', 'their', 'that', 'at', 'upon', 'where', 'on', 'through'}
        }
        self.sentence = lexicon.Sentence(word_order='SVO')
        self.game_lexicon = lexicon.Lexicon(sample_lexicon)

    def test_invalid_vaid_word_orders(self):
        self.assertRaises(AssertionError, lexicon.Sentence, 'vos')
        self.assertRaises(AssertionError, lexicon.Sentence, 'ovs')
        self.assertRaises(AssertionError, lexicon.Sentence, 'osv')
        self.assertRaises(AssertionError, lexicon.Sentence, 'bogus')
        self.assertRaises(AssertionError, lexicon.Sentence, 'b0gus')
        self.assertRaises(AssertionError, lexicon.Sentence, 'b0gu$')
        self.assertRaises(AssertionError, lexicon.Sentence, 'bogus bogus bogus')
        self.assertRaises(AssertionError, lexicon.Sentence, '1234')
        self.assertRaises(AssertionError, lexicon.Sentence, 'svo,')
        self.assertRaises(AssertionError, lexicon.Sentence, '')
        self.assertRaises(AttributeError, lexicon.Sentence, {'svo'})
        self.assertRaises(AttributeError, lexicon.Sentence, 1234)
        self.assertRaises(AttributeError, lexicon.Sentence, ['svo'])
        self.assertRaises(AttributeError, lexicon.Sentence, ('sov',))
        self.assertRaises(AttributeError, lexicon.Sentence, {'svo': ''})

    def test_invalid_data_structure(self):
        """Attempt to build a sentence with an unexpected data structure should raise an error"""
        self.assertRaises(
            AssertionError, self.sentence.build, [{'verb': 'eat'}, ('subject', 'I')]
        )
        self.assertRaises(
            AssertionError, self.sentence.build, [('verb', 'eat', 'sleep', 'rave')]
        )
        self.assertRaises(
            AssertionError, self.sentence.build, ['verb', 'eat', 'sleep', 'rave']
        )
        self.assertRaises(
            AssertionError, self.sentence.build, {'verb', 'eat', 'sleep', 'rave'}
        )
        self.assertRaises(
            AssertionError, self.sentence.build, {'verb': 'eat', 'sleep': 'rave'}
        )
        self.assertRaises(
            lexicon.ParserError, self.sentence.build, [['verb', 'eat'], ('subject', 'I')]
        )
        self.assertRaises(
            lexicon.ParserError, self.sentence.build, [('verb', 'eat'), {'subject', 'I'}]
        )

    def test_invalid_item_types(self):
        """Attempt to build a sentence with unexpected types within pairs should raise an error"""
        self.assertRaises(
            lexicon.ParserError, self.sentence.build, [(1, 'eat'), ('subject', 'I')]
        )
        self.assertRaises(
            lexicon.ParserError, self.sentence.build, [(1, 2), ('subject', 'I')]
        )
        self.assertRaises(
            lexicon.ParserError, self.sentence.build, [(1, 2), (3, 4)]
        )
        self.assertRaises(
            lexicon.ParserError, self.sentence.build, [('verb', ['eat'])]
        )
        self.assertRaises(
            lexicon.ParserError, self.sentence.build, [('verb', {'eat'})]
        )
        self.assertRaises(
            lexicon.ParserError, self.sentence.build, [('verb', 'eat'), ('subject', 3.14)]
        )
        self.assertRaises(
            lexicon.ParserError, self.sentence.build, [('verb', []), ('subject', 'I')]
        )
        self.assertRaises(
            lexicon.ParserError, self.sentence.build, [('verb', {}), ('subject', 'I')]
        )
        self.assertRaises(
            lexicon.ParserError, self.sentence.build, [('verb', set()), ('subject', 'I')]
        )

    def test_build_valid_svo_sentences(self):
        """Build a Subject Verb Object simple sentence (independent clause) out of some of words"""
        # subject is missing so we assume the subject is 'player'
        valid_svo0 = self.game_lexicon.scan_text('Player punch bear')
        valid_svo1 = self.game_lexicon.scan_text('Player punch the bear')
        valid_svo2 = self.game_lexicon.scan_text('Player punch the bear in the face')
        valid_svo3 = self.game_lexicon.scan_text('Player smack bear')
        valid_svo4 = self.game_lexicon.scan_text('Player smack the bear')
        valid_svo5 = self.game_lexicon.scan_text('Player smack the bear in the nose')
        valid_svo6 = self.game_lexicon.scan_text('Player open door')
        valid_svo7 = self.game_lexicon.scan_text('Player open the door')
        valid_svo8 = self.game_lexicon.scan_text('Player punch through the door')
        valid_svo9 = self.game_lexicon.scan_text('Player go through the door')
        valid_svo10 = self.game_lexicon.scan_text('Player go through the door and do some stuff!!')
        valid_svo11 = self.game_lexicon.scan_text('Player go in through the door and do some stuff')
        self.assertEqual(self.sentence.build(valid_svo0), 'player punch bear')
        self.assertEqual(self.sentence.build(valid_svo1), 'player punch bear')
        self.assertEqual(self.sentence.build(valid_svo2), 'player punch bear')
        self.assertEqual(self.sentence.build(valid_svo3), 'player smack bear')
        self.assertEqual(self.sentence.build(valid_svo4), 'player smack bear')
        self.assertEqual(self.sentence.build(valid_svo5), 'player smack bear')
        self.assertEqual(self.sentence.build(valid_svo6), 'player open door')
        self.assertEqual(self.sentence.build(valid_svo7), 'player open door')
        self.assertEqual(self.sentence.build(valid_svo8), 'player punch door')
        self.assertEqual(self.sentence.build(valid_svo9), 'player go door')
        self.assertEqual(self.sentence.build(valid_svo10), 'player go door')
        self.assertEqual(self.sentence.build(valid_svo11), 'player go door')

    def test_build_invalid_svo_sentences(self):
        invalid_svo0 = self.game_lexicon.scan_text('punch bear')
        invalid_svo1 = self.game_lexicon.scan_text('punch the bear')
        invalid_svo2 = self.game_lexicon.scan_text('punch the bear in the face')
        invalid_svo3 = self.game_lexicon.scan_text('smack bear')
        invalid_svo4 = self.game_lexicon.scan_text('smack the bear')
        invalid_svo5 = self.game_lexicon.scan_text('smack the bear in the nose')
        invalid_svo6 = self.game_lexicon.scan_text('open door')
        invalid_svo7 = self.game_lexicon.scan_text('open the door')
        invalid_svo8 = self.game_lexicon.scan_text('punch through the door')
        invalid_svo9 = self.game_lexicon.scan_text('go through the door')
        invalid_svo10 = self.game_lexicon.scan_text('Player go through the wooden, cheap door')
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_svo0)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_svo1)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_svo2)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_svo3)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_svo4)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_svo5)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_svo6)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_svo7)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_svo8)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_svo9)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_svo10)

    def test_build_valid_sov_sentences(self):
        self.sentence = lexicon.Sentence(word_order='sov')
        valid_sov0 = self.game_lexicon.scan_text('Player bear punch')
        valid_sov1 = self.game_lexicon.scan_text('Player the bear punch')
        valid_sov2 = self.game_lexicon.scan_text('Player bear smack')
        valid_sov3 = self.game_lexicon.scan_text('Player the bear smack')
        valid_sov4 = self.game_lexicon.scan_text('Player door open')
        valid_sov5 = self.game_lexicon.scan_text('Player the door open')
        valid_sov6 = self.game_lexicon.scan_text('Player through the door punch')
        valid_sov7 = self.game_lexicon.scan_text('Player through the door go')
        valid_sov8 = self.game_lexicon.scan_text('Player in through the door go')
        self.assertEqual(self.sentence.build(valid_sov0), 'player bear punch')
        self.assertEqual(self.sentence.build(valid_sov1), 'player bear punch')
        self.assertEqual(self.sentence.build(valid_sov2), 'player bear smack')
        self.assertEqual(self.sentence.build(valid_sov3), 'player bear smack')
        self.assertEqual(self.sentence.build(valid_sov4), 'player door open')
        self.assertEqual(self.sentence.build(valid_sov5), 'player door open')
        self.assertEqual(self.sentence.build(valid_sov6), 'player door punch')
        self.assertEqual(self.sentence.build(valid_sov7), 'player door go')
        self.assertEqual(self.sentence.build(valid_sov8), 'player door go')

    def test_build_invalid_sov_sentences(self):
        self.sentence = lexicon.Sentence(word_order='sov')
        invalid_sov0 = self.game_lexicon.scan_text('bear punch')
        invalid_sov1 = self.game_lexicon.scan_text('the bear punch')
        invalid_sov2 = self.game_lexicon.scan_text('bear smack')
        invalid_sov3 = self.game_lexicon.scan_text('the bear smack')
        invalid_sov4 = self.game_lexicon.scan_text('door open')
        invalid_sov5 = self.game_lexicon.scan_text('the door open')
        invalid_sov6 = self.game_lexicon.scan_text('through the door punch')
        invalid_sov7 = self.game_lexicon.scan_text('through the door go')
        invalid_sov8 = self.game_lexicon.scan_text('Player the bear in the face punch')
        invalid_sov9 = self.game_lexicon.scan_text('Player the bear in the nose smack')
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_sov0)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_sov1)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_sov2)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_sov3)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_sov4)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_sov5)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_sov6)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_sov7)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_sov8)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_sov9)

    def test_build_valid_vso_sentences(self):
        self.sentence = lexicon.Sentence(word_order='vso')
        valid_vso0 = self.game_lexicon.scan_text('punch Player bear')
        valid_vso1 = self.game_lexicon.scan_text('punch Player the bear')
        valid_vso2 = self.game_lexicon.scan_text('smack Player bear')
        valid_vso3 = self.game_lexicon.scan_text('smack Player the bear')
        valid_vso4 = self.game_lexicon.scan_text('open Player door')
        valid_vso5 = self.game_lexicon.scan_text('open Player the door')
        valid_vso6 = self.game_lexicon.scan_text('punch Player through the door')
        valid_vso7 = self.game_lexicon.scan_text('go Player through the door')
        valid_vso8 = self.game_lexicon.scan_text('go in Player through the door')
        self.assertEqual(self.sentence.build(valid_vso0), 'punch player bear')
        self.assertEqual(self.sentence.build(valid_vso1), 'punch player bear')
        self.assertEqual(self.sentence.build(valid_vso2), 'smack player bear')
        self.assertEqual(self.sentence.build(valid_vso3), 'smack player bear')
        self.assertEqual(self.sentence.build(valid_vso4), 'open player door')
        self.assertEqual(self.sentence.build(valid_vso5), 'open player door')
        self.assertEqual(self.sentence.build(valid_vso6), 'punch player door')
        self.assertEqual(self.sentence.build(valid_vso7), 'go player door')
        self.assertEqual(self.sentence.build(valid_vso8), 'go player door')

    def test_build_invalid_vso_sentences(self):
        self.sentence = lexicon.Sentence(word_order='vso')
        invalid_vso0 = self.game_lexicon.scan_text('punch bear Player')
        invalid_vso1 = self.game_lexicon.scan_text('punch the bear Player')
        invalid_vso2 = self.game_lexicon.scan_text('smack bear Player')
        invalid_vso3 = self.game_lexicon.scan_text('smack the bear Player')
        invalid_vso4 = self.game_lexicon.scan_text('open door Player')
        invalid_vso5 = self.game_lexicon.scan_text('open the door Player')
        invalid_vso6 = self.game_lexicon.scan_text('punch through the door Player')
        invalid_vso7 = self.game_lexicon.scan_text('go through the door Player')
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_vso0)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_vso1)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_vso2)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_vso3)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_vso4)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_vso5)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_vso6)
        self.assertRaises(lexicon.ParserError, self.sentence.build, invalid_vso7)
