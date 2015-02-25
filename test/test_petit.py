
import unittest
import petit_lisp as pl

from src.parser import Parser

parse = Parser().parse
env = None


def evaluate(s):
    if env is None:
        return pl.evaluate(parse(s))
    else:
        return pl.evaluate(parse(s), env=env)


class TestEvaluate(unittest.TestCase):
    '''Evaluate expressions, using the parse function as a first step'''

    def setUp(self):  # noqa
        pl.global_env = pl.common_env(pl.Env())
        self.assertEqual(True, evaluate("(undefined? x)"))
        evaluate("(load 'src/default_language.lisp)")

    def test_define(self):
        self.assertEqual(None, evaluate("(define x 3)"))
        self.assertEqual(False, evaluate("(undefined? x)"))
        self.assertEqual(7, evaluate("(+ x 4)"))
        self.assertEqual(3, evaluate("x"))

    def test_set(self):
        self.assertEqual(None, evaluate("(define x 3)"))
        self.assertEqual(3, evaluate("x"))
        self.assertEqual(None, evaluate("(set! x 4)"))
        self.assertEqual(8, evaluate("(+ x 4)"))

    def test_lambda(self):
        self.assertEqual(None, evaluate("(define square (lambda (x) (* x x)))"))
        self.assertEqual(9, evaluate("(square 3)"))

    def test_load_python(self):
        # verify that Python module can be imported properly
        global env
        env = pl.global_env
        evaluate('(load-py (quote math))')
        self.assertEqual(4.0, evaluate("(sqrt 16.0)"))
        env = None

    def test_load_python_scope(self):
        pl.loader.load("test/scope_test.lisp")
        self.assertEqual(3, evaluate("pi"))
        from math import pi
        self.assertEqual(pi, evaluate("(mul_pi 1)"))


class TestLogic(unittest.TestCase):

    def setUp(self):  # noqa
        pl.global_env = pl.common_env(pl.Env())
        self.assertEqual(True, evaluate("(undefined? x)"))
        evaluate("(load 'src/default_language.lisp)")

    def test_if(self):
        # test "if", "__True__", "__False__"
        evaluate("(if __True__ (define x 1) (define x 2))")
        self.assertEqual(1, evaluate("x"))
        evaluate("(if __False__ (define x 3) (define x 4))")
        self.assertEqual(4, evaluate("x"))

    def test_not(self):
        # test "if", "__True__", "__False__"
        evaluate("(if (not __True__) (define x 1) (define x 2))")
        self.assertEqual(2, evaluate("x"))
        evaluate("(if (not __False__) (define x 3) (define x 4))")
        self.assertEqual(3, evaluate("x"))

    def test_cond(self):
        # test "cond", ">", ">" ,"="
        expr = """
(define abs (lambda (x)
    (cond ((> x 0) x)
          ((= x 0) 0)
          ((< x 0) (- x)))))"""
        evaluate(expr)
        self.assertEqual(2, evaluate("(abs 2)"))
        self.assertEqual(3, evaluate("(abs -3)"))
        self.assertEqual(0, evaluate("(abs 0)"))

    def test_cond_with_else(self):
        # test "cond", "else", "<="
        expr = """
(define abs2 (lambda (x)
    (cond ((<= x 0) (- x))
          (else x)
          )))"""
        evaluate(expr)
        self.assertEqual(2, evaluate("(abs2 2)"))
        self.assertEqual(3, evaluate("(abs2 -3)"))
        self.assertEqual(0, evaluate("(abs2 0)"))


if __name__ == '__main__':
    unittest.main()
