import action_key_map
import affecter
from heapq import heappush, heappop
import copy

# gets the nodes adjacent to the current affect_vector 
def _puppitor_adjacencies(character_affecter, action_key_map, affect_tuple, goal_emotion, step_multiplier):
    moves = []
    affect_dict = dict(affect_tuple)
    
    affects = affect_dict.keys()
    
    for action, modifier in action_key_map.moves:
        for affect in affects:
            next_state = affect_dict.copy()
            character_affecter.update_affect(next_state, action, modifier, step_multiplier) # make a new affect_vector for the new node and move to the adjacency
            
            node = (tuple(next_state.items()), action, modifier, affecter.get_prevailing_affect(character_affecter, next_state))
            cost = _puppitor_edge_cost(character_affecter, affect_dict, action, modifier, affects, goal_emotion, step_multiplier) # calculate the edge cost of the new node
            
            moves.append((cost, node))
    
    return moves

# calculates the sum of the update values based on the given action and modifier
def _puppitor_edge_cost(character_affecter, affect_vector, action, modifier, affects, goal_emotion, step_multiplier):
    
    #cost = step_value + _affecter_action_modifier_product(character_affecter, action, modifier, goal_emotion, step_value)
    #cost = -step_value * _affecter_action_modifier_product(character_affecter, action, modifier, goal_emotion, step_value)
    
    cost = abs(_affecter_action_modifier_product(character_affecter, action, modifier, goal_emotion, step_multiplier))
    
    #current_affect = character_affecter.current_affect
    
    #if affecter.evaluate_affect_vector(current_affect, affect_vector, goal_emotion) == -1:
    #    cost = abs(cost)
    return cost

def _affecter_action_modifier_product(character_affecter, action, modifier, affect, step_multiplier):
    return character_affecter.affect_rules[affect]['actions'][action] * character_affecter.affect_rules[affect]['modifiers'][modifier] * step_multiplier

def _heuristic(character_affecter, current_affect, affect_vector, goal_emotion):
    heuristic_value = 0

    max_value_nodes = affecter.get_possible_affects(affect_vector)
    
    if max_value_nodes:
        heuristic_value = affect_vector[max_value_nodes[0]] - affect_vector[goal_emotion]
    
    #if goal_emotion in max_value_nodes and current_affect != goal_emotion:
    #    heuristic_value = 100
    #elif goal_emotion not in max_value_nodes:
        """max_action = ''
        max_modifier = ''
        max_action_value = 0
        max_modifier_value = 0
        
        for action, value in character_affecter.affect_rules[goal_emotion]['actions'].items():
            if value == max(character_affecter.affect_rules[goal_emotion]['actions'].values()):
                max_action = action
                max_action_value = value
                
        for modifier, value in character_affecter.affect_rules[goal_emotion]['modifiers'].items():
            if value == max(character_affecter.affect_rules[goal_emotion]['modifiers'].values()):
                max_modifier = modifier
                max_modifier_value = value
        
        dist_to_max = (affect_vector[max_value_nodes[0]] - affect_vector[goal_emotion]) / (_affecter_action_modifier_product(character_affecter, max_action, max_modifier, goal_emotion) - _affecter_action_modifier_product(character_affecter, max_action, max_modifier, max_value_nodes[0]))
        heuristic_value = dist_to_max"""
    #    heuristic_value = 0
    #else:
    #    heuristic_value = -1
    
    return heuristic_value

# A* search for use with Puppitor
# nodes are (affect_vector, action, modifier, prevailing_affect)
# the traditional graph used for A* is split between the affecter and action_key_map modules
def npc_a_star_think(character_affecter, action_key_map, start, goal_emotion, step_multiplier = 1):
    frontier = []
    visited_nodes = []
    cost_so_far = {}
    prev_node = {}
    
    start_node = (tuple(start[0].items()), start[1], start[2], start[3])
    heappush(frontier, (0, start_node))
    prev_node[start_node] = None
    cost_so_far[start_node] = 0
    
    while frontier:
        curr_cost, curr_node = heappop(frontier)

        print(len(frontier))
        if curr_node[3] == goal_emotion:
            path = []
            while curr_node:
                path.append(curr_node)
                curr_node = prev_node[curr_node]
            #path.reverse()
            print(len(path), path)
            return path
        
        for next in _puppitor_adjacencies(character_affecter, action_key_map, curr_node[0], goal_emotion, step_multiplier):
            next_cost, next_node = next
            new_cost = cost_so_far[curr_node] + next_cost + _heuristic(character_affecter, next_node[3], dict(next_node[0]), goal_emotion)
            
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                heappush(frontier, (new_cost, next_node))
                prev_node[next_node] = curr_node
                
    return []
    