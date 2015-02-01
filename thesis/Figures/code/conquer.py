# conquer
all_conditions = defaultdict(set)
...
# Collect all conditions for each must.
# Example: a - proof_constant, X1->F - condition_term
for proof_constant, condition_term in self.musts[atom]:

  proofs_for_atom = []

  for cs_term in self.cs[proof_constant]:
    configuration = match_with_cs_term(
    					cs_term, condition_term)

    if configuration is not None:
      proofs_for_atom.append(configuration)

  if proofs_for_atom:
    all_conditions[(proof_constant, condition_term)] 
    		= proofs_for_atom
  else:
    return None
...
# We have now one or more possible configurations per must.
# Now we need to find configuration that is compatible with at least one
# configuration of all musts.
...
merged_conditions = []
for must in self.musts[atom]:
  merged_conditions = merge_conditions(
  	all_conditions[must], merged_conditions)

  if merged_conditions is None:
    return None
...