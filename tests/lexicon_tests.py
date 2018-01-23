import unittest

from mindgames.lexicon import check_ascii, Lexicon


class LexiconTest(unittest.TestCase):
    def setUp(self):
        self.my_lexicon = Lexicon({
            'subject': {'guido', 'dropbox'},
            'predicate': {'create', 'forge'},
        })

    def test_check_ascii(self):
        self.assertEqual(any(check_ascii(chr(x)) for x in range(125, 255)), True)
        self.assertEqual(all(check_ascii(chr(x)) for x in range(0, 127)), True)
        self.assertEqual(any(check_ascii(chr(x)) for x in range(127, 255)), False)
        self.assertRaises(AssertionError, check_ascii, '')
        self.assertRaises(AssertionError, check_ascii, [])
        self.assertRaises(AssertionError, check_ascii, [1, 2])
        self.assertRaises(AssertionError, check_ascii, ['abc'])
        self.assertRaises(AssertionError, check_ascii, 1234)
        self.assertRaises(AssertionError, check_ascii, {'a': 'test'})

    def test_split_alnum(self):
        self.assertRaises(AssertionError, self.my_lexicon.split_alnum, ' We the best music!!1one  ')
        self.assertRaises(AssertionError, self.my_lexicon.split_alnum, 'We234 t2h1e best mu$sic')
        self.assertRaises(AssertionError, self.my_lexicon.split_alnum, 'd0ll4r$     multiple   s9 ')

        self.assertEqual(
            self.my_lexicon.split_alnum('    1234567890%$#%!@!^&*'),
            ['1234567890']
        )
        self.assertEqual(
            self.my_lexicon.split_alnum('    We the best music!!!one'),
            ['we', 'the', 'best', 'music', 'one']
        )
        self.assertEqual(
            self.my_lexicon.split_alnum('Slap,the,bear   !@#steal honey'),
            ['slap', 'the', 'bear', 'steal', 'honey']
        )
        self.assertEqual(
            self.my_lexicon.split_alnum('Pun,ch,the,  bear  steal honey'),
            ['pun', 'ch', 'the', 'bear', 'steal', 'honey']
        )
        self.assertEqual(
            self.my_lexicon.split_alnum('Pl,ay th,e num,ber game.'),
            ['pl', 'ay', 'th', 'e', 'num', 'ber', 'game']
        )
        self.assertEqual(
            self.my_lexicon.split_alnum('Slap,punch  shout at y"all!'),
            ['slap', 'punch', 'shout', 'at', 'y', 'all']
        )
        self.assertEqual(
            self.my_lexicon.split_alnum('Play,the,number,game!'),
            ['play', 'the', 'number', 'game']
        )
        self.assertEqual(
            self.my_lexicon.split_alnum('Play,the,num,be,r,game,!'),
            ['play', 'the', 'num', 'be', 'r', 'game']
        )
        self.assertEqual(
            self.my_lexicon.split_alnum('PlAy,ThE,NUM,be,R,game,!'),
            ['play', 'the', 'num', 'be', 'r', 'game']
        )
        self.assertEqual(
            self.my_lexicon.split_alnum('A, B, C'),
            ['a', 'b', 'c']
        )

    def test_check_lexicon(self):
        valid_lexicon = {
            'subject': {'i', 'player', 'julia', 'zuck'},
            'verb': {'run', 'go', 'start', 'swipe', 'push', 'acquiescence'},
            'object': {'bear', 'python', 'game', 'door'},
            'constituents': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that'}
        }
        self.assertEqual(self.my_lexicon.check_lexicon(valid_lexicon), True)

        valid_lexicon_bogus_values = {
            'subject': {*(rev[::-1] for rev in {'i', 'player', 'julia', 'zuck'})},
            'verb': {*(rev[::-1] for rev in {'run', 'go', 'start', 'push', 'acquiescence'})},
            'object': {*(rev[::-1] for rev in {'bear', 'python', 'game', 'door'})},
            'constituents': {*(rev[::-1] for rev in {'at', 'or', 'in', 'through', 'over', 'this'})}
        }
        self.assertEqual(self.my_lexicon.check_lexicon(valid_lexicon_bogus_values), True)

        valid_lexicon_bogus_data = {
            'tcejbus': {*(rev[::-1] for rev in {'i', 'player', 'julia', 'zuck'})},
            'breb': {*(rev[::-1] for rev in {'run', 'go', 'start', 'push', 'acquiescence'})},
            'tcejbo': {*(rev[::-1] for rev in {'bear', 'python', 'game', 'door'})},
            'stneutitsnoc': {*(rev[::-1] for rev in {'at', 'or', 'in', 'through', 'over', 'this'})}
        }
        self.assertEqual(self.my_lexicon.check_lexicon(valid_lexicon_bogus_data), True)

        invalid_lexicon_int = {
            'subject': {'i', 1, 'julia', 2},
            'verb': {'run', 20, 'start', 30, 'push', 'acquiescence'},
            'object': {'bear', 'python', 'game', 'door'},
            'constituents': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that'}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_lexicon_int)

        invalid_lexicon_tuple = {
            'subject': {'i', 'player', ('julia', 'moore'), ('zuck', 'mark')},
            'verb': {'run', ('go', 'sprint'), 'start', ('forge', 'craft'), 'push', 'acquiescence'},
            'object': {'bear', 'python', 'game', 'door'},
            'constituents': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that'}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_lexicon_tuple)

        invalid_lexicon_alnum = {
            'subject': {'i', 'player', 'julia', 'zuck', 'z00m', 'm00re'},
            'verb': {'run', 'go', 'start', 'sw1p3', 'push', 'acqu135c3nc3'},
            'object': {'bear', 'python', 'g4m3', 'd00r'},
            'constituents': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that'}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_lexicon_alnum)

        invalid_lexicon_symbols = {
            'subject': {'i', 'player#', 'julia', 'zuck'},
            'verb': {'run', 'go', '$tart', 'swipe', 'push', 'acquiescence'},
            'object': {'bear', 'pyt&on', 'game', 'door'},
            'constituents': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that'}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_lexicon_symbols)

        invalid_lexicon_spaces = {
            'subject': {'i', 'player one', 'julia roberts', 'zuck mark'},
            'verb': {'run', 'go', 'start', 'swipe left', 'push hard', 'acquiescence'},
            'object': {'be ar', 'py th on', 'ga me', 'd o o r'},
            'constituents': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that'}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_lexicon_spaces)

        invalid_lexicon_numbers = {
            'numerals': {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_lexicon_numbers)

        invalid_lexicon_numerals = {
            'numerals': {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_lexicon_numerals)

        invalid_lexicon_uppercase = {
            'subject': {'I', 'PLAYER', 'JULIA', 'ZUCK'},
            'verb': {'RUN', 'GO', 'START', 'SWIPE', 'PUSH', 'ACQUIESENCE'},
            'object': {'BEAR', 'PYTHON', 'GAME', 'DOOR'},
            'constituents': {'AT', 'OR', 'IN', 'THROUGH', 'OVER', 'THIS', 'THE', 'THAT'}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_lexicon_uppercase)

        invalid_lexicon_mixcase = {
            'subject': {'I', 'PlAyEr', 'JuLiA', 'ZuCk'},
            'verb': {'RuN', 'Go', 'StArT', 'SwIpE', 'PuSh', 'AcQuIeSeNcE'},
            'object': {'BeAr', 'PyThOn', 'GaMe', 'DoOr'},
            'constituents': {'aT', 'oR', 'iN', 'THROugh', 'ovER', 'tHIs', 'tHE', 'thAT'}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_lexicon_mixcase)

        invalid_lexicon_dupes = {
            'subject': {'i', 'player', 'julia', 'zuck'},
            'verb': {'run', 'go', 'start', 'swipe', 'push', 'acquiescence'},
            'object': {'bear', 'python', 'game', 'door', 'zuck', 'julia'},  # duplicate entries
            'constituents': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that', 'go'}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_lexicon_dupes)

        invalid_lexicon_dupes2 = {
            'subject': {'i', 'player', 'julia', 'zuck'},
            'verb': {'run', 'go', 'start', 'swipe', 'push', 'acquiescence'},
            'object': {'bear', 'python', 'game', 'door', 'acquiescence'},
            'constituents': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that', 'go'}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_lexicon_dupes2)

        invalid_lexicon_dupes3 = {
            'subject': {'i', 'player', 'julia', 'zuck'},
            'verb': {'run', 'go', 'start', 'swipe', 'push', 'acquiescence'},
            'object': {'bear', 'python', 'game', 'door'},
            'constituents': {'at', 'or', 'in', 'through', 'game', 'that', 'go', 'zuck'}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_lexicon_dupes3)

        invalid_lexicon_keys = {
            'sub ject': {'i', 'player', 'julia', 'zuck'},
            'verb': {'run', 'go', 'start', 'swipe', 'push', 'acquiescence'},
            'object': {'bear', 'python', 'game', 'door'},
            'constituents': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that'}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_lexicon_keys)

        invalid_lexicon_keys2 = {
            'subject': {'i', 'player', 'julia', 'zuck'},
            'verb1': {'run', 'go', 'start', 'swipe', 'push', 'acquiescence'},
            'object': {'bear', 'python', 'game', 'door'},
            'constituents': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that'}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_lexicon_keys2)

        invalid_lexicon_keys3 = {
            'subject': {'i', 'player', 'julia', 'zuck'},
            'verb': {'run', 'go', 'start', 'swipe', 'push', 'acquiescence'},
            'OBJECT': {'bear', 'python', 'game', 'door'},
            'constituents': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that'}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_lexicon_keys3)

        invalid_lexicon_keys4 = {
            'subject': {'i', 'player', 'julia', 'zuck'},
            'verb': {'run', 'go', 'start', 'swipe', 'push', 'acquiescence'},
            'object': {'bear', 'python', 'game', 'door'},
            'CoNsTiTuEnTs': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that'}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_lexicon_keys4)

        invalid_lexicon_keys5 = {
            'subject': {'i', 'player', 'julia', 'zuck'},
            'verb': {'run', 'go', 'start', 'swipe', 'push', 'acquiescence'},
            'object': {'bear', 'python', 'game', 'door'},
            'con$tituent$': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that'}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_lexicon_keys5)

        invalid_nonascii_keys = {
            'subject' + 'çèêëìíîïðñ': {'i', 'player', 'julia', 'zuck'},
            'verb': {'run', 'go', 'start', 'swipe', 'push', 'acquiescence'},
            'object': {'bear', 'python', 'game', 'door'},
            'constituents': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that'}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_nonascii_keys)

        invalid_nonascii_values = {
            'subject': {'i', 'playèêër', 'juliìíîïa', 'zuçk'},
            'verb': {'run', 'gð', 'start', 'swipe', 'push', 'acquiesceñce'},
            'object': {'bear', 'python', 'game', 'door'},
            'constituents': {'at', 'or', 'in', 'through', 'over', 'this', 'the', 'that'}
        }
        self.assertRaises(AssertionError, self.my_lexicon.check_lexicon, invalid_nonascii_values)
