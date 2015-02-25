import unittest
import petit_lisp as pl

from src.parser import Parser

parse = Parser().parse


def evaluate(s):
    return pl.evaluate(parse(s))


class TestBasicLisp(unittest.TestCase):

    def setUp(self):  # noqa
        pl.global_env = pl.common_env(pl.Env())
        self.assertEqual(True, evaluate("(undefined? a)"))

    def test_cons(self):
        expr = "(define a (cons 1 (cons 2 (cons 3 (cons 4 '())))))"
        expr2 = "'(1 2 3 4)"
        evaluate(expr)
        self.assertEqual(evaluate(expr2), evaluate("a"))
        self.assertEqual(False, evaluate("(undefined? a)"))

    def test_cons_error(self):
        expr = "(define a (cons 1 '2))"
        self.assertRaises(ValueError, evaluate, expr)

    def test_car(self):
        expr = "(define a (cons 1 (cons 2 (cons 3 (cons 4 '())))))"
        expr2 = "(car a)"
        evaluate(expr)
        self.assertEqual(1, evaluate(expr2))

    def test_cdr(self):
        expr = "(define a (cons 1 (cons 2 (cons 3 (cons 4 '())))))"
        expr2 = "(cdr a)"
        evaluate(expr)
        self.assertEqual(evaluate("'(2 3 4)"), evaluate(expr2))

    def test_is_atom(self):
        self.assertEqual(True, evaluate("(atom? 3)"))
        self.assertEqual(False, evaluate("(atom? '(1 2 3))"))
