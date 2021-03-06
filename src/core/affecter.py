#
# Affecter is a wrapper around a JSON object based dictionary of affects (see contents of the affect_rules directory for formatting details)
# 
# By default Affecter clamps the values of an Affect_Vector in the range of 0.0 to 1.0 and uses theatrical terminology, consistent with 
# the default keys in gesture_keys.py inside of the actual_action_states dictionary in the Gesture_Interface class
#
import json
import random
import math

class Gesture_Affecter:
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
        self.current_affect = None # changed to None because this value will get updated immediately through the run loop (as long as you call update_affect()

    # discards the stored affect_rules and replaces it with a new rule_file in the above JSON format
    def load_open_rule_file(self, affect_rule_file):
        self.affect_rules = None
        self.affect_rules = json.load(affect_rule_file)
        return

    # for use clamping the updated affect values between a given floor_value and ceil_value
    def _update_and_clamp_values(self, affect_value, affect_update_value, floor_value, ceil_value):
        return max(min(affect_value + affect_update_value, ceil_value), floor_value)
    
    # affect_vector is an Affect_Vector specified by class Affect_Vector in this file
    # the floats correspond to the strength of the expressed affect
    # current_action corresponds to the standard action expressed by a Gesture_Interface instance in its actual_action_states
    # NOTE: clamps affect values between floor_value and ceil_value
    # NOTE: while performing the equilibrium_action the affect values will move toward the equilibrium_value of the given affect_vector
    def update_affect(self, affect_vector, current_action, current_modifier):
        for affect in affect_vector.affects:
            current_action_update_value = self.affect_rules[affect]['actions'][current_action]
            current_modifier_update_value = self.affect_rules[affect]['modifiers'][current_modifier]
            current_equilibrium_value = self.affect_rules[affect]['equilibrium_point']
            
            # move towards resting value specified in affect_vector when updating the action associated with the the 'equilibrium_action'
            if current_action == self.equilibrium_action:
                if affect_vector.affects[affect] > current_equilibrium_value:
                    affect_vector.affects[affect] = self._update_and_clamp_values(affect_vector.affects[affect], -1 * abs(current_modifier_update_value * current_action_update_value), current_equilibrium_value, self.ceil_value)
                elif affect_vector.affects[affect] < current_equilibrium_value:
                    affect_vector.affects[affect] = self._update_and_clamp_values(affect_vector.affects[affect], abs(current_modifier_update_value * current_action_update_value), self.floor_value, current_equilibrium_value)
                else:
                    continue
            else:
                affect_vector.affects[affect] = self._update_and_clamp_values(affect_vector.affects[affect], current_modifier_update_value * current_action_update_value, self.floor_value, self.ceil_value)
        return

    # affect_vector must be an Affect_Vector
    # returns a list of the affects with the highest strength of expression in the given affect_vector
    # allowable_error is used for dealing with the approximate value of floats
    def get_possible_affects(self, affect_vector, allowable_error = 0.00000001):
        prevailing_affects = []
        
        for current_affect in affect_vector.affects:
            if not prevailing_affects:
                prevailing_affects.append(current_affect)
            elif affect_vector.affects[prevailing_affects[0]] < affect_vector.affects[current_affect]:
                prevailing_affects = []
                prevailing_affects.append(current_affect)
            # check if the affect magnitudes are approximately equal
            elif abs(affect_vector.affects[prevailing_affects[0]] - affect_vector.affects[current_affect]) < allowable_error:
                prevailing_affects.append(current_affect)
            #print(current_affect, affect_vector.affects[current_affect])
        #print(prevailing_affects)
        return prevailing_affects

    # chooses the next current affect
    # possible_affects must be a list of strings of affects defined in the .json file loaded into the Affecter instance
    # possible_affects can be generated using the get_possible_affects() function
    # the choice logic is as follows:
    #   pick the only available affect
    #   if there is more than one and the current_affect is in the set of possible_affects pick it
    #   if the current_affect is not in the set but there is at least one affect connected to the current affect, pick from that subset
    #   otherwise randomly pick from the disconnected set of possible affects
    def choose_prevailing_affect(self, possible_affects):
        
        connected_affects = []
        
        if len(possible_affects) == 1:
            self.current_affect = possible_affects[0]
            return self.current_affect

        if self.current_affect in possible_affects:
            return self.current_affect

        for affect in possible_affects:
            if affect in self.affect_rules[self.current_affect]['adjacent_affects']:
                connected_affects.append(affect)
                
        if connected_affects:
            self.current_affect = random.choice(connected_affects)
            return self.current_affect
        else:
            self.current_affect = random.choice(possible_affects)
            return self.current_affect
        
    # wrapper function around the get_possible_affects() to choose_prevailing_affect() pipeline to allow for easier, more fixed integration into other code
    # NOTE: this function is not intended to supercede the useage of both get_possible_affects() and choose_prevailing_affect()
    #       it is here for convenience and if the default behavior of immediately using the list created by get_possible_affects() in choose_prevailing_affect()
    #       is the desired functionality
    def get_prevailing_affect(self, affect_vector, allowable_error = 0.00000001):
        possible_affects = self.get_possible_affects(affect_vector, allowable_error)
        prevailing_affect = self.choose_prevailing_affect(possible_affects)
        return prevailing_affect
        
# a wrapper around a python dictionary to organize affects
class Affect_Vector:
    # affect_names takes a list of strings
    # equilibrium_values is expected to be the rules stored in the affect_rules dictionary of a Gesture_Affecter
    def __init__(self, affect_names, equilibrium_values):
        self.affects = {}
        for affect in affect_names:
            # dictionary with strings specifying affects (as defined in Affecter) as keys and floats as values
            self.affects[affect] = equilibrium_values[affect]['equilibrium_point']
            
