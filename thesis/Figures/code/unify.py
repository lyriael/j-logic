# unify
...
while stack:
  f1, f2 = stack.pop()
  # If the root node is the same (either operation or constant)
  if f1.root.token == f2.root.token:
    # If its a operator, go on. If it's a constant we're done.
    if f1.root.token in ['->', ':']:
      stack.append(
      	(subtree(f1.root.left), subtree(f2.root.left)))
      stack.append(
      	(subtree(f1.root.right), subtree(f2.root.right)))
  # If the root is not the same, either it is a mismatch, 
  # or there is at least one variable.
  elif f1.is_wild() or f2.is_wild():
    result.append((str(f1), str(f2)))
  else:
    return None
return condition_list_to_dict(result)