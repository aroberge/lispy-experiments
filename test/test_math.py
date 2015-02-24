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

prereqs = '''(begin
(define else __True__)
(define #t __True__)
(define #f __False__)
(define null '())
(from-py-load-as 'operator '(eq __eq__))
(define null? (lambda (x) (__eq__ x '())))
(from-py-load-as 'operator '(not_ __not__))
(define not (lambda (x) (__not__ x)))
)
'''


class TestMath(unittest.TestCase):
    '''Evaluate expressions, using the parse function as a first step'''


    def setUp(self):  # noqa
        evaluate(prereqs)
        evaluate("(load 'src/math.lisp)")

    def test_add(self):
        self.assertEqual(7, evaluate("(+ 3 4)"))

    def test_add_floats(self):
        self.assertEqual(7.75, evaluate("(+ 3.25 4.5)"))

    def test_sub(self):
        self.assertEqual(1, evaluate("(- 4 3)"))
        self.assertEqual(-1, evaluate("(- 3 4)"))

    def test_add_many(self):
        self.assertEqual(12, evaluate("(+ 3 4 5)"))

    def test_mul(self):
        self.assertEqual(12, evaluate("(* 3 4)"))
        self.assertEqual(2.4, evaluate("(* 0.6 4)"))

    def test_mul_many(self):
        self.assertEqual(60, evaluate("(* 3 4 5)"))

    def test_div(self):
        self.assertEqual(2.0, evaluate("(/ 8 4)"))

    def test_floor_div(self):
        self.assertEqual(2, evaluate("(// 8 4)"))
        self.assertEqual(2, evaluate("(// 9.1 4)"))

    def test_parse_two_levels(self):
        self.assertEqual(13, evaluate(" (+ (* 3 4) (- 2 1))"))

    def test_parse_three_levels(self):
        self.assertEqual(6, evaluate("(// (+ (* 3 4) (- 2 1)) 2)"))

    def test_define(self):
        self.assertEqual(None, evaluate("(define x 3)"))
        self.assertEqual(7, evaluate("(+ x 4)"))
        self.assertEqual(3, evaluate("x"))

    def test_set(self):
        self.assertEqual(None, evaluate("(define x 3)"))
        self.assertEqual(3, evaluate("x"))
        self.assertEqual(None, evaluate("(set! x 4)"))
        self.assertEqual(8, evaluate("(+ x 4)"))
