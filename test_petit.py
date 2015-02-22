''' usage: python test_petit.py
'''
import mock
import unittest
import petit_lisp as pl

from src.repl import InteractiveInterpreter

parse = pl.parse


def evaluate(s):
    return pl.evaluate(parse(s))


class TestRead(unittest.TestCase):
    '''Ensures that we handle user input correctly'''

    @mock.patch('builtins.input', return_value="(a b c)")
    def test_get_expr_all_at_once(self, input):
        repl = InteractiveInterpreter(pl.evaluate, parse, pl.global_env)
        self.assertEqual("(a b c)", repl.read_expression())

    @mock.patch('builtins.input', side_effect=['(a', 'b', 'c)'])
    def test_get_expr_in_parts(self, input):
        repl = InteractiveInterpreter(pl.evaluate, parse, pl.global_env)
        self.assertEqual("(a b c)", repl.read_expression())


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


class TestEvaluate(unittest.TestCase):
    '''Evaluate expressions, using the parse function as a first step'''

    def setUp(self):  # noqa
        pl.global_env = pl.common_env(pl.Env())
        self.fresh_env = pl.common_env(pl.Env())
        evaluate("(load 'default_language.lisp)")

    def tearDown(self):  # noqa
        pl.global_env = self.fresh_env

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

    def test_lambda(self):
        self.assertEqual(None, evaluate("(define square (lambda (x) (* x x)))"))
        self.assertEqual(9, evaluate("(square 3)"))

    # def test_load_file(self):
    #     pl.loader.load("../define_variable_test.lisp")
    #     self.assertEqual(3, evaluate("x"))

    # def test_load_file_with_comments(self):
    #     pl.loader.load("../comments_test.lisp")
    #     self.assertEqual(49, evaluate("(square 7)"))

    def test_load_python(self):
        # verify that Python module can be imported properly
        evaluate('(load-py (quote math))')
        self.assertEqual(4.0, evaluate("(sqrt 16)"))

    def test_load_python_scope(self):
        pl.loader.load("scope_test.lisp")
        self.assertEqual(3, evaluate("pi"))
        from math import pi
        self.assertEqual(pi, evaluate("(mul_pi 1)"))


class TestLogic(unittest.TestCase):

    def setUp(self):  # noqa
        pl.global_env = pl.common_env(pl.Env())
        self.fresh_env = pl.common_env(pl.Env())
        evaluate("(load 'default_language.lisp)")

    def tearDown(self):  # noqa
        pl.global_env = self.fresh_env

    def test_if(self):
        # test "if", "#t", "#f"
        evaluate("(if #t (define x 1) (define x 2))")
        self.assertEqual(1, evaluate("x"))
        evaluate("(if #f (define x 3) (define x 4))")
        self.assertEqual(4, evaluate("x"))

    def test_not(self):
        # test "if", "#t", "#f"
        evaluate("(if (not #t) (define x 1) (define x 2))")
        self.assertEqual(2, evaluate("x"))
        evaluate("(if (not #f) (define x 3) (define x 4))")
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


class TestLists(unittest.TestCase):

    def setUp(self):  # noqa
        pl.global_env = pl.common_env(pl.Env())

    def test_cons(self):
        expr = "(define a (cons 1 (cons 2 (cons 3 (cons 4 '())))))"
        expr2 = "'(1 2 3 4)"
        evaluate(expr)
        self.assertEqual(evaluate(expr2), evaluate("a"))

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

if __name__ == '__main__':
    unittest.main()
