'''New class based version
'''

import sys
from src.file_loader import FileLoader
from src.python_utils import python_fns
from src.parser import Parser
from src.repl import InteractiveInterpreter
from src.lisps import lisp_procs

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
