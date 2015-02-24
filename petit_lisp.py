'''New class based version
'''

import sys
from src.file_loader import FileLoader
from src.python_utils import python_fns
from src.parser import Parser
from src.repl import InteractiveInterpreter

loader = FileLoader()
STRINGS = {}


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


class Procedure(object):
    "A user-defined procedure."
    def __init__(self, params, body, env,
                 opt_param=False,
                 evaluate=None,
                 env_cls=None):
        self.params, self.body, self.env = params, body, env
        self.opt_param = opt_param
        self.evaluate = evaluate
        self.env_cls = env_cls

    def __call__(self, *args):
        if self.opt_param:
            args = self.pack_args(args)
        return self.evaluate(self.body, self.env_cls(self.params, args, self.env))

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
        # strings are stored with enclosing double quote characters
        obj.__doc__ = s[1:-1]


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
        '''(begin expr1 ... expr_last) ==> evaluates all and returns expr_last'''
        return expr[-1]

    @staticmethod
    def is_atom(atom):
        '''(atom? expr) ==> true if expr is not a list'''
        return not isinstance(atom, list)

    @staticmethod
    def are_equal(val1, val2):
        '''(eq? expr1 expr2) ==> true if both are atoms and equal'''
        return (not isinstance(val1, list)) and (val1 == val2)

    @staticmethod
    def car(*expr):
        '''(car (exp1 exp2 exp3 ...)) ==> exp1'''
        return expr[0][0]

    @staticmethod
    def cdr(*expr):
        '''(car (exp1 exp2 exp3 ...)) ==> (exp2 exp3 ...)'''
        return list(expr[0][1:])

    @staticmethod
    def cons(*expr):
        '''Usage (cons expr list) => (expr list) '''
        if not isinstance(expr[1], list):
            raise ValueError("Second argument of cons must be a list.")
        return [expr[0]] + expr[1]

lisp_procs = {
    'begin': Lisp.begin,
    'atom?': Lisp.is_atom,
    'eq?': Lisp.are_equal,
    'car': Lisp.car,
    'cdr': Lisp.cdr,
    'cons': Lisp.cons
}


def display(s):
    '''Prints a single string.  Strings are enclosed between double quotes
       and do not allow escaped double quote characters'''
    print(s[1:-1])  # strings are stored with enclosing double quote characters


def common_env(env):
    "Add some built-in procedures and variables to the environment."
    env.update({
        '__True__': True,
        '__False__': False,
        '_DEBUG': False,
        'quit': exit,
        'print': display,
        'load': loader.load,
        'set-docstring': Procedure.set_docstring
    })
    env.update(python_fns)
    env.update(lisp_procs)
    return env
exit.__doc__ = "Quits the repl."
global_env = common_env(Env())


def evaluate(x, env=None):
    "Evaluate an expression in an environment."
    if env is None:
        env = global_env
    if isinstance(x, str):            # variable reference
        if x in STRINGS:
            return STRINGS[x]
        return env.find(x)[x]
    elif not isinstance(x, list):     # constant literal
        return x

    if x[0] == 'quote':              # (quote exp), or 'exp
        (_, exp) = x
        return exp
    elif x[0] == 'define':            # (define var exp)
        (_, var, exp) = x
        env[var] = evaluate(exp, env)
    elif x[0] == 'set!':              # (set! var exp)
        (_, var, exp) = x
        env.find(var)[var] = evaluate(exp, env)
    elif x[0] == 'lambda':            # (lambda (params*) body)
        (_, params, body) = x
        opt_param = False
        if '.' in params:
            opt_param = params.index('.')
            params.pop(opt_param)
        return Procedure(params, body, env, opt_param, evaluate, Env)
    elif x[0] == 'cond':              # (cond (p1 e1) ... (pn en))
        for (p, e) in x[1:]:
            if evaluate(p, env):
                return evaluate(e, env)
    elif x[0] == 'if':                # (if test if_true other)
        (_, test, if_true, other) = x
        return evaluate((if_true if evaluate(test, env) else other), env)
    else:                             # ("procedure" exp*)
        exps = [evaluate(exp, env) for exp in x]
        procedure = exps.pop(0)
        try:
            return procedure(*exps, env=env)
        except TypeError:
            return procedure(*exps)

parse = Parser(global_env, STRINGS).parse
loader.evaluate = evaluate
loader.parse = parse


if __name__ == "__main__":
    if len(sys.argv) > 1:
        loader.load(sys.argv[1])
    else:
        loader.load("default_language.lisp")
    interpreter = InteractiveInterpreter(evaluate, parse, global_env)
    interpreter.start()
