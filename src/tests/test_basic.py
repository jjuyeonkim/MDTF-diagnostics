import unittest
from src.util import basic

class TestCanonicalArgName(unittest.TestCase):
    def test_canonical_arg_name(self):
        self.assertEqual(basic.canonical_arg_name('--flag '), 'flag')
        self.assertEqual(basic.canonical_arg_name('--flag-two '), 'flag_two')
        self.assertEqual(basic.canonical_arg_name('-flag-three_3'), 'flag_three_3')

class TestWordWrap(unittest.TestCase):
    def test_word_wrap(self):
        str1 = """
            Here's a multiline test string; we'll test to see
            if the indentation is removed
            and if it
            gets word wrapped to 80 columns, etc.
        """
        str2 = ("Here's a multiline test string; we'll test to see if the "
            "indentation is removed\nand if it gets word wrapped to 80 columns, etc.")
        self.assertEqual(basic.word_wrap(str1), str2)

    def test_word_wrap_multipara(self):
        str1 = """
            Here's a multiline test string; we'll test to see
            if the indentation is removed
            and if it

            gets word wrapped to 80 columns, etc.
            \n\nExplicit para break
        """
        str2 = ("Here's a multiline test string; we'll test to see if the "
            "indentation is removed\nand if it\n\ngets word wrapped to 80 columns,"
            " etc.\n\nExplicit para break")
        self.assertEqual(basic.word_wrap(str1), str2)
