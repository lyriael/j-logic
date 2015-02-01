# atomize
...
# first step: make sum-splits
splits = sum_split(self.formula)

# second step: simplify formula if top operation is !
for formula in splits[:]:
  splits.remove(formula)
  new_formula = simplify_introspection(formula)
  if new_formula:
    splits.append(new_formula)

# third step: remove formulas where '!' is left child of '*'
for formula in splits[:]:
  if has_bad_introspection(formula):
    splits.remove(formula)
return splits