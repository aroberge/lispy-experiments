'''A Read-Eval-Print-Loop with "help" support'''


import sys
import traceback


class InteractiveInterpreter:
    '''A simple interpreter with built-in help'''
    def __init__(self, evaluate, parse, global_env):
        self.evaluate = evaluate
        self.parse = parse
        self.global_env = global_env
        self.started = False
        self.prompt = 'repl> '
        self.prompt2 = ' ... '

    def repl(self):
        "A read-eval-print loop."
        self.started = True
        print("\n  ====  Enter (quit) to end.  ====\n")
        while True:
            inp = self.read_expression()
            if not inp:
                continue
            try:
                val = self.evaluate(self.parse(inp))
                if val is not None:
                    print(self.to_string(val))
            except (KeyboardInterrupt, SystemExit):
                print("\n   Goodbye!")
                return
            except Exception as e:
                print('      {}: {}'.format(type(e).__name__, e))
                if self.global_env["DEBUG"]:
                    traceback.print_exc()

    def read_expression(self):
        '''Reads an expression from a prompt'''
        inp = input(self.prompt)
        open_parens = inp.count("(") - inp.count(")")
        while open_parens > 0:
            inp += ' ' + input(self.prompt2)
            open_parens = inp.count("(") - inp.count(")")

        if inp.startswith(("parse", "help", "dir")):
            self.handle_internally(inp)
            return None
        return inp

    def handle_internally(self, inp):
        if inp.startswith("parse "):
            expr = inp[6:]
            print("     {}\n".format(self.parse(expr)))
        elif inp.startswith("help"):
            help = inp.split()
            if len(help) == 1:
                self.show_variables()
            else:
                self.show_variables(help[1])
        elif inp.startswith("dir"):
            print("\n{}\n".format([x for x in self.global_env.keys()
                                    if not x.startswith("__")]))

    def start(self):
        '''starts the interpreter if not already running'''
        if self.started:
            return
        try:
            self.repl()
        except BaseException:
            # do not use print after KeyboardInterrupt
            raise
            sys.stdout.write("\n      Exiting petit_lisp.")

    def to_string(self, exp):
        "Convert a Python object back into a Lisp-readable string."
        if not isinstance(exp, list):
            if exp is True:
                return "#t"
            elif exp is False:
                return "#f"
            elif isinstance(exp, complex):
                return str(exp).replace('j', 'i')[1:-1]  # remove () put by Python
            return str(exp)
        else:
            return '(' + ' '.join(self.to_string(s) for s in exp) + ')'

    def show_value(self, var, env):
        '''Displays the value of a variable in a given environment or dict'''
        val = env[var]
        if not isinstance(val, (int, float, complex, str)):
            if hasattr(val, '__doc__') and val.__doc__ is not None:
                val = ' '.join(val.__doc__.split('\n')[:3])
        if isinstance(val, str):
            if len(val) > 75:
                val = val[:75].strip() + "..."
        print("  {}: {}".format(var, val))

    def show_variables(self, obj=None):
        '''Inspired by Python's help: shows a list of defined names and
           their values or description
        '''
        env = self.global_env
        if obj == "help":
            print("Usage:  help, help variable, help globals, "
                   "help user-defined")
        elif obj not in [None, "user-defined", "globals"]:
            if obj not in env:
                print("Unknown variable: ", obj)
            else:
                self.show_value(obj, env)
        else:
            names = sorted(env.keys())
            for var in names:
                if var.startswith('__'):
                    continue
                if obj == "user-defined" and var in self.global_env:
                    continue
                elif obj == "globals" and var not in self.global_env:
                    continue
                self.show_value(var, env)
        print()
