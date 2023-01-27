import action_key_map
import affecter
from heapq import heappush, heappop
import copy

# gets the nodes adjacent to the current affect_vector 
# converts the affect_tuple back into a dictionary so it can be used with Puppitor functions
def _puppitor_adjacencies(character_affecter, action_key_map, affect_tuple, goal_emotion, step_multiplier):
    moves = []
    affect_dict = dict(affect_tuple)
    
    affects = affect_dict.keys()
    
    # make a list of every action and modifier combination and those nodes to the adjacency list
    for action, modifier in action_key_map.moves:
        next_state = affect_dict.copy()
        character_affecter.update_affect(next_state, action, modifier, step_multiplier) # make a new affect_vector for the new node and move to the adjacency
        
        node = (tuple(next_state.items()), action, modifier, affecter.get_prevailing_affect(character_affecter, next_state))
        cost = _puppitor_edge_cost(character_affecter, affect_dict, action, modifier, affects, goal_emotion, step_multiplier) # calculate the edge cost of the new node
        
        moves.append((cost, node))

    return moves

# calculates the magnitude of the change in value of the goal_emotion in affect_vector
def _puppitor_edge_cost(character_affecter, affect_vector, action, modifier, affects, goal_emotion, step_multiplier):
    
    #cost = step_value + _affecter_action_modifier_product(character_affecter, action, modifier, goal_emotion, step_value)
    #cost = -step_value * _affecter_action_modifier_product(character_affecter, action, modifier, goal_emotion, step_value)
    
    cost = abs(_affecter_action_modifier_product(character_affecter, action, modifier, goal_emotion, step_multiplier))
    
    #current_affect = character_affecter.current_affect
    
    #if affecter.evaluate_affect_vector(current_affect, affect_vector, goal_emotion) == -1:
    #    cost = abs(cost)
    return cost

# multiplies the action, modifier, and step_multiplier values together
def _affecter_action_modifier_product(character_affecter, action, modifier, affect, step_multiplier):
    return character_affecter.affect_rules[affect]['actions'][action] * character_affecter.affect_rules[affect]['modifiers'][modifier] * step_multiplier

# calculate the distance between the maximum value in affect_vector and the value of the goal_emotion
def _heuristic(current_affect, affect_vector, goal_emotion):
    heuristic_value = 0

    max_value_nodes = affecter.get_possible_affects(affect_vector)
    
    if max_value_nodes:
        heuristic_value = affect_vector[max_value_nodes[0]] - affect_vector[goal_emotion]
    
    #if goal_emotion in max_value_nodes and current_affect != goal_emotion:
    #    heuristic_value = 100
    #elif goal_emotion not in max_value_nodes:
        #max_action = ''
        #max_modifier = ''
        #max_action_value = 0
        #max_modifier_value = 0
        
        #for action, value in character_affecter.affect_rules[goal_emotion]['actions'].items():
        #    if value == max(character_affecter.affect_rules[goal_emotion]['actions'].values()):
        #        max_action = action
        #        max_action_value = value
                
        #for modifier, value in character_affecter.affect_rules[goal_emotion]['modifiers'].items():
        #    if value == max(character_affecter.affect_rules[goal_emotion]['modifiers'].values()):
        #        max_modifier = modifier
        #        max_modifier_value = value
        
        #dist_to_max = (affect_vector[max_value_nodes[0]] - affect_vector[goal_emotion]) / (_affecter_action_modifier_product(character_affecter, max_action, max_modifier, goal_emotion) - _affecter_action_modifier_product(character_affecter, max_action, max_modifier, max_value_nodes[0]))
        #heuristic_value = dist_to_max"""
    #    heuristic_value = 0
    #else:
    #    heuristic_value = -1
    
    return heuristic_value

# A* search for use with Puppitor
# nodes are (affect_vector, action, modifier, prevailing_affect)
# start is a tuple of (affect_vector, action, modifier, prevailing_affect)
# NOTE: the traditional graph definition used for A* is split between the affecter and action_key_map modules
# NOTE: affect_vectors must be converted to tuples as part of making a node because nodes must be hashable
def npc_a_star_think(character_affecter, action_key_map, start, goal_emotion, step_multiplier = 1, max_queue_size = 18000):
    frontier = [] # queue of nodes to visit
    visited_nodes = [] # list of nodes that have been visited
    cost_so_far = {} # the smallest cost to reach a given node
    prev_node = {} # the node we traveled to the current node from
    
    start_node = (tuple(start[0].items()), start[1], start[2], start[3])
    heappush(frontier, (0, start_node))
    prev_node[start_node] = None
    cost_so_far[start_node] = 0
    
    while frontier or len(frontier) < max_queue_size:
        curr_cost, curr_node = heappop(frontier)

        # if the node's prevailing affect is the affect we want to express, get the path there
        if curr_node[3] == goal_emotion:
            path = []
            while curr_node:
                # add the number of steps it actually takes to reach the estimated distance
                counter = 0
                while counter < step_multiplier:
                    counter += 1
                    path.append(curr_node)
                curr_node = prev_node[curr_node]

            print('path length: ', len(path), '\nfrontier length: ', len(frontier))
            return path
        
        # check every adjacent node of the current node and if it is a new node or a more efficient way to get to next_node, add it to the frontier
        for next in _puppitor_adjacencies(character_affecter, action_key_map, curr_node[0], goal_emotion, step_multiplier):
            next_cost, next_node = next
            new_cost = cost_so_far[curr_node] + next_cost + _heuristic(next_node[3], dict(next_node[0]), goal_emotion)
            
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                heappush(frontier, (new_cost, next_node))
                prev_node[next_node] = curr_node
              
    print('NO PATH FOUND WITHIN QUEUE SIZE LIMITS')
    return []
    