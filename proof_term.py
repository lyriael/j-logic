import parser
import re
formulas = ['(a+b):B', '(a+b):A', 'b!:(b:B)', '(b!+c):(b:B)', '((a+b)+c):C']


class ProofTerm(object):

    def __init__(self, expression):
        self.type = self.get_type(expression)
        return

    def is_constant(self):
        return self.type == 'CONSTANT'

    def is_sum(self):
        return self.type == 'SUM'

    def is_bang(self):
        return self.type == 'BANG'

    def set_type(self):
        #todo: somehow find out what typ this is.
        self.type = self._types[0]
        return self._types[0]

    def get_left(self):
        assert self.type == 'SUM', "Cannot get left if Proof Term is not of type SUM."
        #todo: read left variable
        return False

    def get_right(self):
        assert self.type == 'SUM', "Cannot get right if Proof Term is not of type SUM."
        #todo: read right variable
        return False

    def remove_bang(self):
        assert self.type == 'BANG', "Cannot remove BANG if Proof Term is not of type Bang."
        #todo: read inner
        return self

    def get_type(self, expression):
        constants = re.findall('\w', expression)
        operations = re.findall('\W', expression)
        if len(operations) == 0 and len(constants) == 1:
            return 'CONSTANT'
        else:
            return 'something'