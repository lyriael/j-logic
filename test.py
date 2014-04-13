'''Using http://www.laurentluce.com/posts/binary-search-tree-library-in-python/ as help '''

class Node:

    parent = None;
    left = None;
    right = None;

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
        elif self.is_eclamation:
            print("It's a strange \"!\"")




class Term:

    def __init__(self,c,A):
        self.proof_constant = c;
        self.axiom = A;

    def to_String(self):
        return self.proof_constant +":"+ self.axiom


t=Term("(!f)", "A->B");
print(t.to_String());
