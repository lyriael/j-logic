# Tree.musts 1/2
...
if len(proof_term.to_s()) == 1: # constant
    consts.append((proof_term.to_s(), subformula))
else:
    if proof_term.root.token == '*':
        left = proof_term.subtree(
            proof_term.root.left).to_s()
        right = proof_term.subtree(
            proof_term.root.right).to_s()
        temp.append(Tree('('+left+
            ':(X'+str(v_count)+'->'+subformula+'))'))
        temp.append(Tree('('+right+
            ':X'+str(v_count)+')'))
        v_count += 1
    elif proof_term.root.token == '!':
        left = proof_term.subtree(
            f.root.left.right).to_s()
        s = '('+left+':X'+str(v_count)+')'
        temp.append(Tree(s))
        swaps.append((subformula, s))
        v_count += 1
# Tree.compare 1/
...
elif cs_node.token[0] == 'X':
    # condition containing Xs and constants.
    if 'X' in orig_node.to_s():
        t = (cs_node.token, orig_node.to_s())
        conditions.append(t)
    # wild
    else:
        wilds[cs_node.token] = orig_node.to_s()
# unresolved 'Y' in cs-subtree to corresponding 'X' in orig
elif orig_node.token[0] == 'X' 
        and ('Y' in cs_node.to_s() or 'X' in cs_node.to_s()):
    # condition containing Xs, Ys and/or constants.
    t = (orig_node.token, cs_node.to_s())
    conditions.append(t)
# normal wild config. 
# the option for 'Y' is for the special case that a Y-wild formula 
# is compared with a formula containing only constants.
elif orig_node.token[0] == 'X' or orig_node.token[0] == 'Y':
    wilds[orig_node.to_s()] = cs_node.to_s()
else:
    # no match possible
    conditions, wilds = None, None