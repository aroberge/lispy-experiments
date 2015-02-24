'''Basic parser for lisp expressions'''

import re


class Parser:
    "Parse a Lisp expression from a string"
    def __init__(self, STRINGS=None):  # noqa
        self.regex = re.compile('"(?:[^"])*"')
        self.STRINGS = STRINGS
        if STRINGS is None:
            self.STRINGS = {}

    def parse(self, s):
        "Parse a Lisp expression from a string."
        return self.convert_to_list(self.tokenize(s))

    def convert_to_list(self, tokens):
        "Converts a sequence of tokens into a list"
        if len(tokens) == 0:
            raise SyntaxError('convert_to_list: unexpected EOF while reading')
        token = tokens.pop(0)
        if '(' == token:
            lst = []
            while tokens[0] != ')':
                lst.append(self.convert_to_list(tokens))
            tokens.pop(0)   # pop off ')'
            return lst
        elif ')' == token:
            raise SyntaxError('convert_to_list: unexpected )')
        elif "'" == token:
            return ['quote', self.convert_to_list(tokens)]
        else:
            return self.atomize(token)

    def atomize(self, token):
        "Converts individual tokens to numbers if possible"
        for conversion in [int, float, complex]:
            try:
                # Python uses j instead of i for sqrt(-1)
                return conversion(token.replace('i', 'j'))
            except ValueError:
                pass
        return token

    def tokenize(self, s):
        "Convert a string into a list of tokens."
        if '"' in s:
            s = self.replace_strings(s)
        return s.replace("(", " ( ").replace(")", " ) ").replace("'", " ' ").split()

    def replace_strings(self, s):                       # noqa
        '''replace double quoted strings by # followed by their Python id
           and stores the correspondance in the global environment

           Does not make allowance for escaped double quote (\") character.'''
        quoted_strings = re.findall(self.regex, s)
        for s_ in quoted_strings:
            symbol = "#{}".format(id(s_))
            s = s.replace(s_, symbol)
            self.STRINGS[symbol] = s_
        return s
