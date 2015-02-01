# musts
...
if proof_term.root.is_leaf():
  consts.append((str(proof_term), str(subformula)))
elif proof_term.root.token == '*':
  left = subtree(proof_term.root.left)
  right = subtree(proof_term.root.right)
  todo.append(Tree('(%s:(X%s->%s))' % 
  	(str(left), str(v_count), str(subformula))))
  todo.append(Tree('(%s:X%s)' % 
  	(str(right), str(v_count))))
  v_count += 1
elif proof_term.root.token == '!':
  left = subtree(f.root.left.right)
  s = '(%s:X%s)' % (str(left), str(v_count))
  todo.append(Tree(s))
  assignments.append((str(subformula), s))
  v_count += 1