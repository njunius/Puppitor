import collections
import action_key_map
import affecter

def update_from_path(path):
    node = path.pop()
    action = node[1]
    modifier = node[2]
    
    return (action, modifier)
    
def maximize_minimize_affect_vector(affect_vector, char_affecter, goal_emotion):
    for affect in affect_vector:
        if affect == goal_emotion:
            affect_vector[affect] = 0
        else:
            affect_vector[affect] = 1
        
    affecter.get_prevailing_affect(char_affecter, affect_vector)
    return

def apply_print_path(path, char_affecter, character_av, step_value, verbose):
    while path:
        action, modifier = update_from_path(path)
        char_affecter.update_affect(character_av, action, modifier)
        
        if verbose:
            print('\naction and modifier: ' + action + ', ' + modifier)
            print('\ncharacter affect vector: ', character_av)
    return

# 
def print_run_info(step_value, emotional_goal, affect_vector):
    print()
    print('\nstep value: ', step_value, '\nemotional goal: ', emotional_goal)
    print('\nstarting affect_vector: ', affect_vector, '\n')
    
    return
    
# finds the number of nodes it takes for the prevailing affect in a path to change
# note the path npc_a_star produces is in reverse order
def find_first_affect_change(path):
    start_node = path[len(path) - 1]
    init_affect = start_node[3]
    count = 0
    curr_affect = None
    
    for node in reversed(path):
        curr_affect = node[3]
        if curr_affect != init_affect:
            return (count, init_affect, curr_affect)
            
        count += 1
    
    return (count, init_affect, curr_affect)
    
# returns a list of each place in the given path where the expressed affect changes
# the info in each list element returned is:
#   - number of steps from the last place the expressed affect changed
#   - the initial expressed affect
#   - the previous expressed affect
#   - the currently expressed affect
def find_all_affect_changes(path):
    delta_info = collections.namedtuple('delta_info', ['count', 'init_affect', 'prev_affect', 'curr_affect', 'curr_action', 'curr_mod'])
    
    start_node = path[len(path) - 1]
    init_affect = start_node[3]
    prev_affect = init_affect
    prev_action = start_node[1]
    prev_mod = start_node[2]
    count = 0
    curr_affect = None
    
    affect_changes = []
    
    for node in reversed(path):
        curr_action = node[1]
        curr_mod = node[2]
        curr_affect = node[3]
        if curr_affect != prev_affect:
            temp_node = delta_info._make((count, init_affect, prev_affect, curr_affect, curr_action, curr_mod))
            affect_changes.append(temp_node)
            prev_affect = curr_affect
            prev_action = curr_action
            prev_mod = curr_mod
        
        elif curr_action != prev_action or curr_mod != prev_mod:
            temp_node = delta_info._make((count, init_affect, prev_affect, curr_affect, curr_action, curr_mod))
            affect_changes.append(temp_node)
            prev_affect = curr_affect
            prev_action = curr_action
            prev_mod = curr_mod
        
        count += 1
    
    return affect_changes