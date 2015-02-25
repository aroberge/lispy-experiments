
DEBUG = False


class FileLoader:
    """Execute a "lisp" program in a file"""

    def __init__(self, evaluate=None, parse=None):
        self.parse = parse
        self.evaluate = evaluate

    def load(self, filename):
        '''loads, parse and evaluate/executes a lisp program'''
        if DEBUG:
            print("    --> Loading {}".format(filename))

        with open(filename, "r") as f:
            program = f.readlines()
        rps = self.running_paren_sums(program)
        full_line = ""
        for ((linenumber, paren_sum), program_line) in zip(rps, program):
            if ";" in program_line:
                program_line = program_line.split(";")[0]
            program_line = program_line.strip()
            full_line += program_line + " "
            if paren_sum == 0 and full_line.strip():
                try:
                    val = self.evaluate(self.parse(full_line))
                    if val is not None:
                        print(val)
                except Exception as e:
                    print("\n    An error occured in loading %s:" % filename)
                    print("line {}:\n{}".format(linenumber, full_line))
                    print('      {}: {}'.format(type(e).__name__, e))
                    break
                full_line = ""

    def running_paren_sums(self, program):
        """
        Map the lines in the list program to a list whose entries contain
        a running sum of the per-line difference between the number of '('
        parentheses and the number of ')' parentheses.
        """
        total = 0
        rps = []
        for linenumber, line in enumerate(program):
            total += line.count("(")-line.count(")")
            rps.append((linenumber, total))
        return rps
