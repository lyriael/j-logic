if proof_term.root.token == '*':
    left = proof_term.subtree(proof_term.root.left).to_s()
    right = proof_term.subtree(proof_term.root.right).to_s()
    temp.append(Tree('('+left+':(X'+str(v_count)+'->'+subformula+'))'))
    temp.append(Tree('('+right+':X'+str(v_count)+')'))
    v_count += 1
    
elif proof_term.root.token == '!':
    left = proof_term.subtree(f.root.left.right).to_s()
    s = '('+left+':X'+str(v_count)+')'
    temp.append(Tree(s))
    swaps.append((subformula, s))
    v_count += 1