class Variable(object):

    def __init__(self, representation):
        self.rep = representation

    def get_representation(self):
        return self.rep


class Substitution(Variable):

    operator = {'+': False, '!': False}

    def __init__(self, variables, type):
        Variable.__init__(self, "xyz") #todo generate representation
        self.variables = variables
        self.operator[type] = True

    def is_bang(self):
        return self.operator['!']

    def is_sum(self):
        return self.operator['+']


class Constant(Variable):

    def __init__(self):
        Variable.__init__(self, "xzy")