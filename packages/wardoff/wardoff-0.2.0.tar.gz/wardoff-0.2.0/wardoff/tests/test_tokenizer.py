import textwrap
import unittest

from wardoff import tokenizer
from wardoff.tests import utils as tutils


class TestWardoffTokenizer(unittest.TestCase):
    expected = textwrap.dedent(
        """\
        TokenInfo(type=62 (ENCODING), string='utf-8', start=(0, 0), end=(0, 0), line='')
        TokenInfo(type=1 (NAME), string='def', start=(1, 0), end=(1, 3), line="def boom(name='yo', age=1):")
        TokenInfo(type=1 (NAME), string='boom', start=(1, 4), end=(1, 8), line="def boom(name='yo', age=1):")
        TokenInfo(type=54 (OP), string='(', start=(1, 8), end=(1, 9), line="def boom(name='yo', age=1):")
        TokenInfo(type=1 (NAME), string='name', start=(1, 9), end=(1, 13), line="def boom(name='yo', age=1):")
        TokenInfo(type=54 (OP), string='=', start=(1, 13), end=(1, 14), line="def boom(name='yo', age=1):")
        TokenInfo(type=3 (STRING), string="'yo'", start=(1, 14), end=(1, 18), line="def boom(name='yo', age=1):")
        TokenInfo(type=54 (OP), string=',', start=(1, 18), end=(1, 19), line="def boom(name='yo', age=1):")
        TokenInfo(type=1 (NAME), string='age', start=(1, 20), end=(1, 23), line="def boom(name='yo', age=1):")
        TokenInfo(type=54 (OP), string='=', start=(1, 23), end=(1, 24), line="def boom(name='yo', age=1):")
        TokenInfo(type=2 (NUMBER), string='1', start=(1, 24), end=(1, 25), line="def boom(name='yo', age=1):")
        TokenInfo(type=54 (OP), string=')', start=(1, 25), end=(1, 26), line="def boom(name='yo', age=1):")
        TokenInfo(type=54 (OP), string=':', start=(1, 26), end=(1, 27), line="def boom(name='yo', age=1):")
        TokenInfo(type=4 (NEWLINE), string='', start=(1, 27), end=(1, 28), line='')
        TokenInfo(type=0 (ENDMARKER), string='', start=(2, 0), end=(2, 0), line='')"""  # noqa
    )

    def test_tokenizer_against_raw_code(self):

        # using in the given code help us to use common expected code between
        # the raw test and the tests against file
        results = "\n".join(
            map(repr, tokenizer.tokenizer("def boom(name='yo', age=1):"))
        )
        self.assertEqual(self.expected, results)

    def test_tokenizer_against_line_of_file(self):
        # input file is our sample code file at line 52 which correspond to
        # our expected result
        infile = "{}+52".format(
            str(tutils.TEST_BASE_DIR.joinpath("sample.py"))
        )
        results = "\n".join(map(repr, tokenizer.tokenizer(infile)))
        function_name = results.split("\n")[2]
        self.assertEqual(
            "TokenInfo(type=1 (NAME), string='boom', start=(1, 4), end=(1, 8), line='def boom(name=\"yo\", age=1):\\n')",  # noqa
            function_name,
        )
