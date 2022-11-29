#
# Affecter is a wrapper around a JSON object based dictionary of affects (see contents of the affect_rules directory for formatting details)
# 
# By default Affecter clamps the values of an affect vector (dictionaries built using make_affect_vector) in the range of 0.0 to 1.0 and uses theatrical terminology, consistent with 
# the default keys in action_key_map.py inside of the actual_action_states dictionary in the Action_Key_Map class
#
import json
import random
import math

class Affecter:
    def __init__(self, affect_rules_file, affect_floor = 0.0, affect_ceiling = 1.0, equilibrium_action = 'resting'):
        # affect_rules_file must be a valid open file with the following format:
        # ['affect']['type']['action']
        # NOTE 'type' is either 'actions' or 'modifiers'
        # each ['action'] has a corresponding update value
        # ['affect']['adjacent_affects'] contains a list of other valid affect names that are used to create a directed graph of emotional affects for a character
        # ['affect']['equilibrium_point'] is the value that affect tends towards when performing the specified equilibrium_action
        self.affect_rules = json.load(affect_rules_file)

        self.floor_value = affect_floor
        self.ceil_value = affect_ceiling
        self.equilibrium_action = equilibrium_action
        self.current_affect = None 
        
        for affect in self.affect_rules:
            entry_equilibrium = self.affect_rules[affect]['equilibrium_point']
            
            if not self.current_affect:
                self.current_affect = affect
            elif entry_equilibrium > self.affect_rules[self.current_affect]['equilibrium_point']:
                self.current_affect = affect
                
        # choosing affect lists
        self.connected_affects = []

    # discards the stored affect_rules and replaces it with a new rule_file in the above JSON format
    def load_open_rule_file(self, affect_rule_file):
        self.affect_rules = None
        self.affect_rules = json.load(affect_rule_file)
        return

    # for use clamping the updated affect values between a given floor_value and ceil_value
    def _update_and_clamp_values(self, affect_value, affect_update_value, floor_value, ceil_value):
        return max(min(affect_value + affect_update_value, ceil_value), floor_value)
    
    # affect_vector is a dictionary built using make_affect_vector()
    # the floats correspond to the strength of the expressed affect
    # current_action corresponds to the standard action expressed by an Action_Key_Map instance in its actual_action_states
    # NOTE: clamps affect values between floor_value and ceil_value
    # NOTE: while performing the equilibrium_action the affect values will move toward the equilibrium_value of the Affecter
    # value_multiplier allows the base value and value_add to be multiplied by a specified value
    # value_add allows the base value to be added to be offset by a specified amount
    # the defaults of value_multiplier and value_add do not scale the base values at all
    def update_affect(self, affect_vector, current_action, current_modifier, value_multiplier = 1, value_add = 0):
        for affect in affect_vector:
            
            current_action_update_value = self.affect_rules[affect]['actions'][current_action]
            current_modifier_update_value = self.affect_rules[affect]['modifiers'][current_modifier]
            current_equilibrium_value = self.affect_rules[affect]['equilibrium_point']
            current_affect_value = affect_vector[affect] # is a float or int so cannot be used to update values in the actual affect vector
            
            value_to_add = value_multiplier * (current_modifier_update_value * current_action_update_value) + value_add
            
            # move values towards resting value by the equilibrium_point associated with affect
            if current_action == self.equilibrium_action:
                if current_affect_value > current_equilibrium_value:
                    affect_vector[affect] = self._update_and_clamp_values(current_affect_value, -1 * abs(value_to_add), current_equilibrium_value, self.ceil_value)
                elif current_affect_value < current_equilibrium_value:
                    affect_vector[affect] = self._update_and_clamp_values(current_affect_value, abs(value_to_add), self.floor_value, current_equilibrium_value)
                
            else:
                affect_vector[affect] = self._update_and_clamp_values(current_affect_value, value_to_add, self.floor_value, self.ceil_value)
        return

# affect_vector should be a dictionary built using make_affect_vector()
# returns a list of the affects with the highest strength of expression in the given affect_vector
def get_possible_affects(affect_vector):
    return [key for key, value in affect_vector.items() if value == max(affect_vector.values())]
    

# chooses the next current affect
# possible_affects must be a list of strings of affects defined in the .json file loaded into the Affecter instance
# possible_affects can be generated using the get_possible_affects() function
# the choice logic is as follows:
#   pick the only available affect
#   if there is more than one and the current_affect is in the set of possible_affects pick it
#   if the current_affect is not in the set but there is at least one affect connected to the current affect, pick from that subset
#   otherwise randomly pick from the disconnected set of possible affects
# TODO: if picking from connected affects return the one that has been at maximum value the longest and is still valid
def choose_prevailing_affect(affecter, possible_affects, random_floor = 0, random_ceil = 100):
    del affecter.connected_affects[:]

    if len(possible_affects) == 1:
        affecter.current_affect = possible_affects[0]
        return affecter.current_affect
    if affecter.current_affect in possible_affects:
        return affecter.current_affect
        
    curr_affect_adjacency_weights = affecter.affect_rules[affecter.current_affect]['adjacent_affects']
    
    for affect in possible_affects:
        if affect in curr_affect_adjacency_weights.keys():
            affecter.connected_affects.append(affect)
            
    if affecter.connected_affects:
        affecter.current_affect = choose_weighted_random_affect(affecter.connected_affects, curr_affect_adjacency_weights, affecter.current_affect, random_floor, random_ceil)
        return affecter.current_affect
    else:
        affecter.current_affect = random.choice(possible_affects)
        return affecter.current_affect
    
# wrapper function around the get_possible_affects() to choose_prevailing_affect() pipeline to allow for easier, more fixed integration into other code
# NOTE: this function is not intended to supercede the useage of both get_possible_affects() and choose_prevailing_affect()
#       it is here for convenience and if the default behavior of immediately using the list created by get_possible_affects() in choose_prevailing_affect()
#       is the desired functionality
def get_prevailing_affect(affecter, affect_vector):
    possible_affects = get_possible_affects(affect_vector)
    prevailing_affect = choose_prevailing_affect(affecter, possible_affects)
    return prevailing_affect
        
# returns a chosen affect from connected_affects based on curr_affect_adjacency_weights
# if all values in curr_affect_adjacency_weights are 0, then no weighting is used and a random affect is chosen
# connected_affects is a list of strings
# curr_affect_adjacency_weights is a dictionary of <string, int> 
# current_affect is a string and is the default affect if there are no adjacencies
# random_floor and random_ceil are integers
def choose_weighted_random_affect(connected_affects, curr_affect_adjacency_weights, current_affect, random_floor = 0, random_ceil = 100):

    random_choice = random.randint(random_floor, random_ceil)
            
    # weighted random choice of the connected affects to the current affect
    # a weight of 0 is ignored
    for affect in connected_affects:
    
        curr_affect_weight = curr_affect_adjacency_weights[affect]
        if curr_affect_weight > 0 and random_choice <= curr_affect_weight:
            return affect
        random_choice -= curr_affect_weight

    # if all weights are zero, just pick randomly and if there are no adjacencies just keep doing what you are told
    if(connected_affects):
        return random.choice(connected_affects)
    else:
        return current_affect
        
# evaluates a given affect_vector based on the difference in values between the goal_emotion and the highest valued affects
def evaluate_affect_vector(current_affect, affect_vector, goal_emotion):
    score = 0
    goal_emotion_val = affect_vector[goal_emotion]
    
    # get all the keys for the max valued affects
    max_affects = get_possible_affects(affect_vector)
    
    if current_affect == goal_emotion:
        score += 1
    elif len(max_affects) > 1 and goal_emotion in max_affects and current_affect != goal_emotion:
        score -= 1
    else:
        for affect in affect_vector:
            if affect != goal_emotion:
                score += goal_emotion_val - affect_vector[affect]
    
    return score

# affect_names takes a list of strings
# equilibrium_values is expected to be the rules stored in the affect_rules dictionary of an Affecter
def make_affect_vector(affect_names, equilibrium_values):
    
    affect_vector = {}
    
    for affect in affect_names:
        affect_vector[affect] = equilibrium_values[affect]['equilibrium_point']
    
    return affect_vector

