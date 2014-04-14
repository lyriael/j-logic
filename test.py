'''Using http://www.laurentluce.com/posts/binary-search-tree-library-in-python/ as help '''


class Node:

    parent = None
    left = None
    right = None

    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data
        print("A node has been made.")

    def children(self):
        if self.is_axiom:
            print("It's a axiom")
        elif self.is_union:
            print("It's a union")
        elif self.is_bang:
            print("It's a strange \"!\"")


class Formula:             # Node --> Formula

    is_axiom = False     # is_leaf

    def __init__(self, c, A):
        self.proof_term = c
        self.subformula = A

    def is_axiom_of_cs(self, cs):
        return cs[self.proof_constant] == self.axiom

    def to_String(self):
        return self.proof_constant + ":" + self.axiom

    def is_provable(self, cs):
        if self.proof_term.is_constant();
           return self.is_axiom_of_cs(self, cs)
        elif self.proof_term.is_sum();
            left = Formula(self.proof_term.get_left(), self.subformula)
            right = Formula(self.proof_term.get_right(), self.subformula)
            return left.is_provable(cs) or right.is_provable(cs)
        elif self.proof_term.is_bang()
            #todo


        return True


class Proof_Term:

    def __init__(self, t):
        self.term = t

    def is_constant(self):
        return True

    def is_sum(self):
        return True

    def is_bang(self):
        return True

    def get_left(self):
        #todo
        return False

    def get_right(self):
        #todo
        return False





class Tree:

    def __init__(self, cs, term):
        self.root = term
        self.leaves.push(term)
        self.cs = cs

    def grow_child(term):
        return 42

cs = {"c1": "¬A", "c2": "A->B"}
t = Term("(!f)", "A->B")
print(t.to_String())