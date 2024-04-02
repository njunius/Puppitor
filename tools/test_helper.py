import collections
import action_key_map
import affecter

delta_info = collections.namedtuple('delta_info', ['count', 'init_affect', 'prev_affect', 'curr_affect', 'curr_action', 'curr_mod'])

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

def verbose_print(path):
    '''while path:
        action, modifier = update_from_path(path)
        char_affecter.update_affect(character_av, action, modifier)
        
        if verbose:
            print('\naction and modifier: ' + action + ', ' + modifier)
            print('\nprevailing affect: ' + affecter.get_prevailing_affect(char_affecter, character_av))
            print('\ncharacter affect vector: ', character_av)'''
    for node in path:
        print('\naction and modifier: ' + node[1] + ', ' + node[2])
        print('\nprevailing affect: ' + node[3])
        print('\ncharacter affect vector: ', node[0])
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
    start_node = path[0]
    init_affect = start_node[3]
    prev_affect = init_affect
    prev_action = start_node[1]
    prev_mod = start_node[2]
    count = 0
    curr_affect = None
    
    affect_changes = []
    
    for node in path:
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
    
    
# helper function to create the initial state for pathfinding using different search functions wrapped around an A* like interface
# start is the tuple passed to the main wrapper function
# curr_node is a local variable to the main wrapper function which tracks the current Puppitor state
# result_path is a list that will contain the final path between to affect vectors
def set_up_path(start, result_path):
    result_path = []
    start_node = (tuple(start[0].items()), start[1], start[2], start[3])
    print(start_node)
    result_path.append(start_node)
    
    return result_path
    
    
def make_path_seg(result_path, char_affecter, action, mod, step_value):
    
    start_path_seg = result_path[-1] # build this next segment of the path starting from the end of the current path
    print(start_path_seg)
    index_av = dict(start_path_seg[0]) # unwrap the tuple back into a mutable affect vector
    
    for i in range(0, step_value):
        new_av = index_av.copy()
        char_affecter.update_affect(new_av, action, mod)
        
        new_node = (tuple(new_av.items()), action, mod, affecter.get_prevailing_affect(char_affecter, new_av))
        result_path.append(new_node)
        #print(new_node[3], goal_emotion)
        index_av = new_av
    
    return

    
# returns a list of each move made by the greedy_search
# start is the initial state for the greedy_search to start from
# start is formatted just like an A* node:
#   - node[0] = affect_vector
#   - node[1] = action
#   - node[2] = modifier
#   - node[3] = prevailing affect
# key_map is a Puppitor action_key_map corresponding to the one used to make the greedy search instance
# char_affecter is the affecter of the character whose rules will be used as the search domain
# step_value controls how frequently the Greedy Search is allowed to re-evaluate its location in expressive space
def make_greedy_path(start, greedy_search, key_map, char_affecter, goal_emotion, step_value):
    result_path = []
    
    result_path = set_up_path(start, result_path)
    
    curr_node = result_path[0]
    
    action = ''
    mod = ''
    
    # as long as we aren't already expressing our emotional goal
    while curr_node[3] != goal_emotion:
        
        new_av = dict(curr_node[0])
        
        action, mod = greedy_search.think(key_map, char_affecter, new_av, goal_emotion) # pick an action and modifier to perform for the next step_value times
        
        make_path_seg(result_path, char_affecter, action, mod, step_value)
            
        curr_node  = result_path[-1]
        
    return result_path
    
def make_mcts_path(start, uct_think, key_map, char_affecter, goal_emotion, step_value, itermax = 2000, rollout_max = 50):
    result_path = []
    
    result_path = set_up_path(start, result_path)
    
    curr_node = result_path[0]
    
    action = ''
    mod = ''
    
    # as long as we aren't already expressing our emotional goal
    while curr_node[3] != goal_emotion:
        new_av = dict(curr_node[0])
        
        root_mcts_node = dict(curr_node[0])
        action, mod = uct_think(root_mcts_node, key_map, char_affecter, goal_emotion, itermax, rollout_max, step_value)
        
        make_path_seg(result_path, char_affecter, action, mod, step_value)
            
        curr_node  = result_path[-1]
    
    return result_path
    