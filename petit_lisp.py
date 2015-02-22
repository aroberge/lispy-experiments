'''New class based version
'''

import operator
import sys
from src.file_loader import FileLoader
from src import python_utils
from src.parser import Parser
from src.repl import InteractiveInterpreter

exit.__doc__ = "Quits the repl."

loader = FileLoader()


class Lisp:
    '''Grouping some basic lisp procedures into logical unit

        The following static methods are invoked within a lisp program as:
            (proc expr1 expr2 expr3 ...)
        which we denote below as (proc exprs*). They are then evaluated
            exps = [evaluate(exp, env) for exp in exprs*]
        and dispatched to the relevant static method as
            proc(*exps)
    '''

    @staticmethod
    def begin(*expr):
        '''Usage: (begin expr1 ... expr_last) ==> evaluates all and returns expr_last'''
        return expr[-1]

    @staticmethod
    def is_atom(atom):
        '''Usage: (atom? expr) ==> true if expr is not a list'''
        return not isinstance(atom, list)

    @staticmethod
    def are_equal(val1, val2):
        '''Usage: (eq? expr1 expr2) ==> true if both are atoms and equal'''
        return (not isinstance(val1, list)) and (val1 == val2)

    @staticmethod
    def car(*expr):
        '''Usage: (car (exp1 exp2 exp3 ...)) ==> exp1'''
        return expr[0][0]

    @staticmethod
    def cdr(*expr):
        '''Usage: (car (exp1 exp2 exp3 ...)) ==> (exp2 exp3 ...)'''
        return list(expr[0][1:])


def display(s):
    '''Prints a single string.  Strings are enclosed between double quotes
       and do not allow escaped double quote characters'''
    print(s[1:-1])  # strings are stored with enclosing double quote characters


def common_env(env):
    "Add some built-in procedures and variables to the environment."
    env = Env()
    env.update({
        'begin': Lisp.begin,
        'atom?': Lisp.is_atom,
        'eq?': Lisp.are_equal,
        'car': Lisp.car,
        'cdr': Lisp.cdr,
        '/': operator.truediv,
        '//': operator.floordiv,
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '=': operator.eq,
        'quit': exit,
        '#t': True,
        '#f': False,
        'not': operator.not_,
        'load': loader.load,
        'DEBUG': False,
        'nil': [],
        'print': display,
        'load-py': python_utils.load_module,
        'from-py-load': python_utils.from_module_load,
        'from-py-load-as': python_utils.from_module_load_variable_as,
        'with-py-inst': python_utils.with_instance,
        'set-docstring': Procedure.set_docstring
    })
    return env


class Procedure(object):
    "A user-defined procedure."
    def __init__(self, params, body, env, opt_param=False):
        self.params, self.body, self.env = params, body, env
        self.opt_param = opt_param

    def __call__(self, *args):
        if self.opt_param:
            args = self.pack_args(args)
        return evaluate(self.body, Env(self.params, args, self.env))

    def pack_args(self, args):
        '''ensures that any extra arguments are packed into a list'''
        if len(args) < self.opt_param:
            raise Exception("Not enough arguments supplied to procedure.")
        elif len(args) == self.opt_param:
            newargs = list(args)
            newargs.append([])
            return tuple(newargs)
        elif ((len(args) > self.opt_param + 1) or
                (not isinstance(args[self.opt_param], list))):
            newargs = [arg for arg in args[:self.opt_param]]
            newargs.append(list(args[self.opt_param:]))
            return tuple(newargs)
        else:
            return args

    @staticmethod
    def set_docstring(obj, s):
        '''Sets the docstring of an object; useful for user-defined procedures'''
        obj.__doc__ = s


class Env(dict):
    "An environment: a dict of {'var': val} pairs, with an outer Env."

    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, var):
        "Find the innermost Env where var appears."
        if var in self:
            return self
        elif self.outer is not None:
            return self.outer.find(var)
        else:
            raise ValueError("{} is not defined".format(var))

global_env = common_env(Env())


def evaluate(x, env=global_env):
    "Evaluate an expression in an environment."
    if isinstance(x, str):            # variable reference
        return env.find(x)[x]
    elif not isinstance(x, list):     # constant literal
        return x

    first = x[0]
    if first == 'quote':              # (quote exp), or 'exp
        (_, exp) = x
        return exp
    elif first == 'cons':              # (cons exp1 exp2)
        (_, exp1, exp2) = x
        _x = evaluate(exp2, env)
        if not isinstance(_x, list):
            _x = [_x]
        return [evaluate(exp1, env)] + _x
    elif first == 'define':            # (define var exp)
        (_, var, exp) = x
        env[var] = evaluate(exp, env)
    elif first == 'set!':              # (set! var exp)
        (_, var, exp) = x
        env.find(var)[var] = evaluate(exp, env)
    elif first == 'lambda':            # (lambda (params*) body)
        (_, params, body) = x
        opt_param = False
        if '.' in params:
            opt_param = params.index('.')
            params.pop(opt_param)
        return Procedure(params, body, env, opt_param)
    elif first == 'cond':              # (cond (p1 e1) ... (pn en))
        for (p, e) in x[1:]:
            if evaluate(p, env):
                return evaluate(e, env)
    elif first == 'if':                # (if test if_true other)
        (_, test, if_true, other) = x
        return evaluate((if_true if evaluate(test, env) else other), env)
    elif first == 'null?':             # (null? exp)
        (_, exp) = x
        return evaluate(exp, env) == []
    else:                             # ("procedure" exp*)
        exps = [evaluate(exp, env) for exp in x]
        procedure = exps.pop(0)
        try:
            return procedure(*exps, env=env)
        except TypeError:
            return procedure(*exps)


parse = Parser(global_env).parse
loader.evaluate = evaluate
loader.parse = parse


if __name__ == "__main__":
    if len(sys.argv) > 1:
        loader.load(sys.argv[1])
    else:
        loader.load("default_language.lisp")
    interpreter = InteractiveInterpreter(evaluate, parse, global_env)
    interpreter.start()
