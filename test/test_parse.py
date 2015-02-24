
import unittest

from src.parser import Parser

parse = Parser().parse


class TestParse(unittest.TestCase):
    '''Ensures that we parse expressions correctly, transforming them into
       the appropriate "list of lists" representation'''

    def test_parse_add(self):
        self.assertEqual(['+', 3, 4], parse("(+ 3 4)"), msg="basic")
        self.assertEqual(['+', 3, 4], parse(" ( + 3  4  ) "), msg="extra spaces")

    def test_parse_add_more(self):
        self.assertEqual(['+', 3, 4, 5], parse(" ( + 3 4 5)"), msg="more args")

    def test_parse_two_levels(self):
        self.assertEqual(['*', ['+', 3, 4], ['-', 2, 1]], parse(" (* ( + 3 4) (- 2 1))"))
