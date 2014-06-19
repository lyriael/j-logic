from formula import Formula
from helper import parse
from stack import Stack


class ProofSearch:

    def __init__(self, cs, formula):
        '''
        expect a string as formula
        '''
        self._cs = cs
        self._formula = Formula(formula)
        self._to_proof = []

    def devide(self):
        stack = Stack()
        stack.push(self._formula)
        while stack.has_element():
            f = stack.pop()
            case = f.proof_term.top_operation()
            if case == '+':
                stack.push(f.get_left_split())
                stack.push(f.get_right_split())
            elif case == '!':
                if f.bang_removable():
                    stack.push(f.remove_bang())
            elif case == '*':
                proof_term = f.proof_term
                self._wander(stack, proof_term)
            elif case == 'const':
                self._to_proof.append(f)

    def _wander(self, stack, f):
        '''
        Asserts that top operation of f is '*' and only 'proof_term' is given.
        Not recursive.
        If '+' or '!' are within f, f is split and its parts are pushed back to the stack.
        If nothing can be changed, f is added to the _to_proof array.
        '''
        #todo: remove as soon as it works in formula
        nodes = f.collect()
        for node in nodes:
            if node.token() == '+':
                stack.push(Formula(node.get_left_split()))
                stack.push(Formula(node.get_right_split()))
                return
            elif node.top_operation() == '!':
                if node.is_left() and node.parent().top_operation() == '*':
                    stack.push(node.remove())
                    return
        self._to_proof.append(f)

    def is_provable(self):
        proof_term = self._formula.proof_term()
        subformula = self._formula.subformula()

        case = proof_term.top_operation()  # should be one of +, !, * or const

        if case == '+':
            left = self._formula.left_operand()

        if case == 'const' and self._formula.is_in(self._cs):
            return True
        else:
            return False



