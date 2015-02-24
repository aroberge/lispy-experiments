import unittest

from src.parser import Parser
from src.file_loader import FileLoader

loader = FileLoader()
parse = Parser().parse
loader.parse = parse
global_env = {}


def evaluate(x, env=global_env):
    if isinstance(x, str):
        return env[x]
    elif not isinstance(x, list):
        return x
    elif x[0] == 'define':
        (_, var, exp) = x
        env[var] = evaluate(exp, env)
loader.evaluate = evaluate


class TestLoadFile(unittest.TestCase):
    '''Simple test to see if we load files correctly'''

    def test_load_file(self):
        loader.load("test/define_variable_test.lisp")
        self.assertEqual(3, evaluate(parse("x")))
