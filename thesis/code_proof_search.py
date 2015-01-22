x_index = int(condition[0][1:])-1
config_term = config[x_index]
condition_term = update_condition_with_x(condition[1], config)

# If config_term is not empty, it contains only constants. In that case we can determine all
# X's and Y's that occur in condition_term if there are any. If there are no wilds simply check
# if config_term and condition_term are the same, else get all remaining X's and Y's.
if config_term != '':
    conds, wilds = Tree.compare(Tree(condition_term).root, 
                    Tree(config_term).root, [], {})
    if wilds is not None:
        assert conds == []
        y_wilds = {}
        for key in wilds:
            if key[0] == 'X':
                i = int(key[1:])-1
                if wilds[key] == config[i] or config[i] == '':
                    config[i] = wilds[key]
                else:
                    return None, None, None
            elif key[0] == 'Y':
                y_wilds[key] = wilds[key]
        return config, None, None if y_wilds == {} else y_wilds
    else:
        return None, None, None
# If config_term is empty the only chance to solve the condition is, if the condition consists
# only of constants. If that is the case it can be put into config and the condition may be
# dismissed. Else nothing more can be done.
elif config_term == '':
    if 'X' not in condition_term and 'Y' not in condition_term:
        config[x_index] = condition_term
        return config, None, None
    else:
        return config, (condition[0], condition_term), None
# apply_all_conditions
todo_conditions = list(conditions)
updated_config = config
remaining_conditions = []

while todo_conditions:
    current_condition = todo_conditions.pop()
    updated_config, mod_conditions, y_wilds = 
        apply_condition(config, current_condition)

    if updated_config:
        if mod_conditions:
            remaining_conditions.append(mod_conditions)
        if y_wilds:
            updated_conditions = 
                get_all_with_y(todo_conditions, y_wilds.keys()) 
                 + get_all_with_y(remaining_conditions, y_wilds.keys())
            for key in y_wilds:
                updated_conditions = 
                    update_y(updated_conditions, key, y_wilds[key])
            todo_conditions = todo_conditions + updated_conditions
    else:
        break
return updated_config, remaining_conditions