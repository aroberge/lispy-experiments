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
