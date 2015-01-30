stack = [(Tree(f1), Tree(f2))]
result = []
while len(stack) > 0:
    current = stack.pop()
    # If the root node is the same (either operation or constant)
    if current[0].root.token == current[1].root.token:
        if current[0].root.token in ['->', ':']:
            stack.append((current[0].subtree(current[0].root.left), 
                current[1].subtree(current[1].root.left)))
            stack.append((current[0].subtree(current[0].root.right), 
                current[1].subtree(current[1].root.right)))
        else:
            pass
    # If the root is not the same, either it is a mismatch, or there are variables.
    else:
        if (_has_no_wilds(current[0].to_s()) and _has_wilds(current[1].root.token)) or \
            (_has_no_wilds(current[1].to_s()) and _has_wilds(current[0].root.token)):
            result.append((current[0].to_s(), current[1].to_s()))
        elif _has_wilds(current[0].to_s()) and _has_wilds(current[1].to_s()):
            assert _has_wilds(current[0].root.token) or _has_wilds(current[1].root.token)
            result.append((current[0].to_s(), current[1].to_s()))
        else:
            return None
return condition_list_to_dict(result)