'''Note: this file will contain various flavours of lisp'''


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

    @staticmethod
    def cons(*expr):
        '''Usage (cons expr list) => (expr list) '''
        _x = expr[1]
        if not isinstance(_x, list):
            _x = [_x]
        return [expr[0]] + _x
