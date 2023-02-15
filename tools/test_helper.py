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

def print_run_info(step_value, emotional_goal, affect_vector):
    print()
    print('\nstep value: ', step_value, '\nemotional goal: ', emotional_goal)
    print('\nstarting affect_vector: ', affect_vector, '\n')
    
    return