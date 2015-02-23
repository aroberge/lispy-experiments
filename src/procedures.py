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
