__author__ = 'lyriael'

import Node from tree

tests = ['(c+(a+b))', '!a']
r = Node.make('(c+(a+b))')[0]
print("PREORDER")
r.preorder()
print("INORDER")
r.inorder()

for i in Node.make('(c+(a+b))'):
    print("looking at: " + i.token)
    print("left: " + str(i.has_left()))
    print("right: " + str(i.has_right()))
    print("root: " + str(i.is_root()))
    print("leaf: " + str(i.is_leaf()))
    print("-----------------------")

print(r)
