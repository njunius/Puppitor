import action_key_map
import affecter
from heapq import heappush, heappop
import copy
import sys

# gets the nodes adjacent to the current affect_vector 
# converts the affect_tuple back into a dictionary so it can be used with Puppitor functions
def _puppitor_adjacencies(character_affecter, action_key_map, affect_tuple, goal_emotion, step_multiplier):
    moves = []
    affect_dict = dict(affect_tuple)
    
    affects = affect_dict.keys()
    
    # make a list of every action and modifier combination and those nodes to the adjacency list
    for action, modifier in action_key_map.moves:
        next_state = affect_dict.copy()
        
        max_value_affects = affecter.get_possible_affects(next_state)
        step_distance = step_multiplier
        goal_max_dist = _calc_distance_between_affects(next_state, max_value_affects[0], goal_emotion)
        
        if goal_max_dist < step_multiplier:
            step_distance = goal_max_dist
        
        character_affecter.update_affect(next_state, action, modifier, step_multiplier) # make a new affect_vector for the new node and move to the adjacency
        
        node = (tuple(next_state.items()), action, modifier, affecter.get_prevailing_affect(character_affecter, next_state))
        cost = _puppitor_edge_cost(character_affecter, affect_dict, action, modifier, affects, goal_emotion, step_distance) # calculate the edge cost of the new node
        
        moves.append((cost, node))

    return moves

# calculates the magnitude of the change in value of the goal_emotion in affect_vector
def _puppitor_edge_cost(character_affecter, affect_vector, action, modifier, affects, goal_emotion, step_multiplier):
    
    goal_delta = abs(_affecter_action_modifier_product(character_affecter, action, modifier, goal_emotion, step_multiplier))
    
    max_val_affects = affecter.get_possible_affects(affect_vector)
    
    curr_max_delta = abs(_affecter_action_modifier_product(character_affecter, action, modifier, max_val_affects[0], step_multiplier))
    
    #cost = abs(_affecter_action_modifier_product(character_affecter, action, modifier, goal_emotion, step_multiplier))

    cost = abs(curr_max_delta - goal_delta)
    return cost

# multiplies the action, modifier, and step_multiplier values together
def _affecter_action_modifier_product(character_affecter, action, modifier, affect, step_multiplier):
    return character_affecter.affect_rules[affect]['actions'][action] * character_affecter.affect_rules[affect]['modifiers'][modifier] * step_multiplier

# calculate the heuristic value of an affect_vector based on:
#   the goal_emotion value
#   the highest valued affect(s)
#   what the current prevailing affect is
def _heuristic(current_affect, affect_vector, goal_emotion):
    heuristic_value = 0

    max_value_nodes = affecter.get_possible_affects(affect_vector)
    
    if goal_emotion in max_value_nodes and current_affect != goal_emotion: # return the furthest distance possible if the our goal_emotion is maxed out but not the prevailing affect
        heuristic_value = sys.maxsize
        return heuristic_value
    
    if max_value_nodes:
        heuristic_value = _calc_distance_between_affects(affect_vector, max_value_nodes[0], goal_emotion)
    
    return heuristic_value
    
# calculate the distance between two affect values in an affect_vector
def _calc_distance_between_affects(affect_vector, first_affect, second_affect):
    return affect_vector[first_affect] - affect_vector[second_affect]

# constructs the path to be returned by A* search
# each argument corresponds to the variable of the same name in npc_a_star_think()
# analysis is a flag which enables full path reconstruction for the purposes of analyzing the output as it is slower than partial reconstruction that is the default behavior
def _construct_path(curr_node, prev_node, character_affecter, step_multiplier, frontier, analysis = False):
    path = []
    while curr_node:
        # add the number of steps it takes to reach the estimated distances
        counter = 0
        while counter < step_multiplier:
            counter += 1
            path.append(curr_node)
            if prev_node[curr_node] == None:
                break
        curr_node = prev_node[curr_node]
        
    final_path = path
    
    if analysis:
        reconst_path = []
        counter = 0
        for curr_node in reversed(path):
            temp_av = dict(curr_node[0])
            
            if counter > 0:
                temp_av = dict(reconst_path[-1][0])
                character_affecter.update_affect(temp_av, curr_node[1], curr_node[2])
                
            updated_node = (temp_av, curr_node[1], curr_node[2], affecter.get_prevailing_affect(character_affecter, temp_av))
            reconst_path.append(updated_node)
            counter += 1
        final_path = reconst_path
    
    print('path length: ', len(final_path), '\nfrontier length: ', len(frontier))
    return final_path

# A* search for use with Puppitor
# nodes are (affect_vector, action, modifier, prevailing_affect)
# start is a tuple of (affect_vector, action, modifier, prevailing_affect)
# NOTE: the traditional graph definition used for A* is split between the affecter and action_key_map modules
# NOTE: affect_vectors must be converted to tuples as part of making a node because nodes must be hashable
def npc_a_star_think(character_affecter, action_key_map, start, goal_emotion, step_multiplier = 1, max_queue_size = 18000, analysis = False):
    frontier = [] # queue of nodes to visit
    visited_nodes = [] # list of nodes that have been visited
    cost_so_far = {} # the smallest cost to reach a given node
    prev_node = {} # the node we traveled to the current node from
    
    start_node = (tuple(start[0].items()), start[1], start[2], start[3])
    heappush(frontier, (0, start_node))
    prev_node[start_node] = None
    cost_so_far[start_node] = 0
    
    while frontier and len(frontier) < max_queue_size:
        curr_cost, curr_node = heappop(frontier)

        # if the node's prevailing affect is the affect we want to express, get the path there
        if curr_node[3] == goal_emotion:
            return _construct_path(curr_node, prev_node, character_affecter, step_multiplier, frontier, analysis)
        
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
    