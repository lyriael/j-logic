# simplify
...
# get all (X1, Fi)
fs = conditions.pop(var, [])
# If there are no conditions for var, we're done.
if not fs: return []

# Preprocess fs: if there is any condition where X1 occurs in Fi then we have a contradiction
# except if precisely X1 == Fi
for fi in fs:
  if var in fi and var != fi:
    return None
...
# Unify each with another: Gives new conditions.
# If any match returns None, we have a contradiction and stop.
new_conditions = defaultdict(set)
for f1, f2 in itertools.combinations(fs, 2):
  conditions_unify = unify(f1, f2)
  if conditions_unify is None:
    return None
  new_conditions.update(conditions_unify)

# Keep one of the (X1, Fi) and replace all X1 
# in the Fis of the other Variables.
# X1 will only occur as the chosen one.
chosen = fs.pop()
for key in conditions:
  conditions[key] = set(
  	item.replace(var, chosen) for item in conditions[key])

# Add the chose one and the new conditions to old conditions.
# Collect new variables to return.
conditions[var].update([chosen])
new_vars = []
for key in new_conditions:
  if not conditions[key]:
    new_vars.append(key)
  conditions[key].update(new_conditions[key])
...
# Clean redundant entries like {'X1': {'X1'}}
for key in conditions:
  if key in conditions[key]:
    conditions[key].remove(key)