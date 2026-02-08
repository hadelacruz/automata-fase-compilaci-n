#Autor: Humberto Alexander de la Cruz - 23735

def construir_dfa(root, followpos):
    print("Construcción del DFA:")
    
    states = {}
    unmarked_states = [frozenset(root.firstpos)]
    states_map = {unmarked_states[0]: 'A'}
    dfa_transitions = {}
    
    while unmarked_states:
        current_set = unmarked_states.pop(0)
        state_name = states_map[current_set]
        
        next_set = set()
        for p in current_set:
            if p != 3:
                next_set.update(followpos[p])
        
        if next_set:
            next_set_frozen = frozenset(next_set)
            if next_set_frozen not in states_map:
                states_map[next_set_frozen] = chr(ord(state_name) + 1)
                unmarked_states.append(next_set_frozen)
            dfa_transitions[(state_name, 'd')] = states_map[next_set_frozen]
    
    print("  Estados y transiciones:")
    all_states = sorted(states_map.values())
    for state in all_states:
        matching_set = [k for k, v in states_map.items() if v == state][0]
        is_final = 3 in matching_set
        final_mark = " (Final)" if is_final else ""
        print(f"    Estado {state}{final_mark}: {set(matching_set)}")
        for (s, char), next_s in dfa_transitions.items():
            if s == state:
                print(f"      --{char}--> {next_s}")
    print()
    
    return states_map, dfa_transitions
