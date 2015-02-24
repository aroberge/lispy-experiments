import mock
import unittest

from src.repl import InteractiveInterpreter


class TestRead(unittest.TestCase):
    '''Ensures that we handle user input correctly'''

    @mock.patch('builtins.input', return_value="(a b c)")
    def test_get_expr_all_at_once(self, input):
        repl = InteractiveInterpreter()
        self.assertEqual("(a b c)", repl.read_expression())

    @mock.patch('builtins.input', side_effect=['(a', 'b', 'c)'])
    def test_get_expr_in_parts(self, input):
        repl = InteractiveInterpreter()
        self.assertEqual("(a b c)", repl.read_expression())
