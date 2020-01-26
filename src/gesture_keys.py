# gesture_interface contains the default keybindings for performing gestures in a dictionary
# the dictionary is modeled on Ren'Py's keymap
# the class also wraps the flags for detecting if an action is being done
#
# the possible_action_states dict is used to keep track of all interpreted actions being done and is updated based on keys and buttons pressed
#
# the actual_action_states is broken into modifier states and actions
# only one action can be happening at a time
# only one modifier can be active at a time
# modifiers update independently from actions
# actions update independently from modifiers
#
# the Gesture_Interface class ASSUMES THE FIRST ITEM OF action_states IS THE DEFAULT AND CURRENT ACTION AT INITIALIZATION TIME
# the Gesture_Interface class ASSUMES THE LAST ITEM OF modifier_states IS THE DEFAULT AND CURRENT MODIFIER AT INITIALIZATION TIME
#
# action_states and modifier_states cannot have any shared values
#
# default_keys takes pygame key and button values
# Gesture_Interface assumes that the first M items in default_keys correspond to the items in action_states where M is the number of items - 1 in action_states
# Gesture_Interface assumes that the last N items in default_keys correspond to the items in modifier states where N is the number of items - 1 in modifier_states
#
import pygame

class Gesture_Interface:
    def __init__(self, action_states = ['resting', 'open_flow', 'closed_flow', 'projected_energy'], modifier_states = ['tempo_up', 'tempo_down', 'neutral'], default_keys = [pygame.K_SPACE, 3, 1, pygame.K_LSHIFT, pygame.K_LCTRL]):
        """self.keymap = { 
                        'open_flow' : [pygame.K_SPACE],
                        'closed_flow' : [3], # references right mouse button
                        'projected_energy' : [1], # references left mouse button
                        'tempo_up' : [pygame.K_LSHIFT],
                        'tempo_down' : [pygame.K_LCTRL]
                      }"""
                      
        for action in action_states:
            if action in modifier_states:
                print('usage: you cannot have an action that is also a modifier')
                return
        
        if len(action_states) - 1 + len(modifier_states) - 1 != len(default_keys):
            print('usage: there must be a key or button bound to each non default action or modifier')
        
        self.keymap = {}
        for i in range(1, len(action_states)):
            self.keymap[action_states[i]] = [default_keys[i - 1]]
        for i in range(0, len(modifier_states) - 1):
            
            self.keymap[modifier_states[i]] = [default_keys[i + len(action_states) - 1]]
        
        print(self.keymap)
        
        # flags corresponding to actions being specified by the user input
        # FOR INPUT DETECTION USE ONLY
        # MULTIPLE ACTIONS AND MODIFIER STATES CAN BE TRUE
        """self.possible_action_states = {
                        'open_flow' : False,
                        'closed_flow' : False,
                        'projected_energy' : False,
                        'tempo_up' : False,
                        'tempo_down' : False
                      }"""
        self.possible_action_states = {}
        for i in range(1, len(action_states)):
            self.possible_action_states[action_states[i]] = False
        for i in range(0, len(modifier_states) - 1):
            self.possible_action_states[modifier_states[i]] = False
        # flags used for specifying the current state of actions for use in updating a character's physical affect
        # FOR SEMANTIC USE
        # ONLY ONE ACTION AND MODIFIER STATE CAN BE TRUE
        """self.actual_action_states = {
                        'actions' : {'resting' : True, 'open_flow' : False, 'closed_flow' : False, 'projected_energy' : False},
                        'modifiers' : {'tempo_up' : False, 'tempo_down' : False, 'neutral' : True}
                        #'resting' : True, # the default action (should be set to True when no other non-modifier states are true)
                        #'open_flow' : False, # an action
                        #'closed_flow' : False, # an action
                        #'projected_energy' : False, # an action
                        #'tempo_up' : False, # a modifier state
                        #'tempo_down' : False # a modifier state
                      }"""
        self.actual_action_states = {
                                        'actions' : {},
                                        'modifiers' : {}
                                    }
        for category in self.actual_action_states:
            if category == 'actions':
                for i in range(0, len(action_states)):
                    if i == 0:
                        self.actual_action_states['actions'][action_states[i]] = True
                    else:
                        self.actual_action_states['actions'][action_states[i]] = False
            if category == 'modifiers':
                for i in range(0, len(modifier_states)):
                    if i == len(modifier_states) - 1:
                        self.actual_action_states['modifiers'][modifier_states[i]] = True
                    else:
                        self.actual_action_states['modifiers'][modifier_states[i]] = False
        # allows toggling of keys rather than press and hold when true
        self.toggle = False

        # ALL must have a value corresponding to a key in the actual_action_states dictionary of actions or modifiers
        # for the current usage both current_action and default_action are initialized to 'resting' 
        # for the current usage both current_modifier and default_modifier are initialized to 'neutral'
        self.current_action = action_states[0] # modified when actual_action_states is called on an action
        self.default_action = action_states[0] # should not be modified outside of this initialization
        self.current_modifier = modifier_states[-1] # modified when actual_action_states is called on a modifier
        self.default_modifier = modifier_states[-1] # should not be modified outside of this initialization
        
    # USED FOR UPDATING BASED ON KEYBOARD INPUTS
    # updates a specified state to a new boolean value
    def update_possible_states(self, state_to_update, new_value):
        for state in self.possible_action_states:
            if state == state_to_update:
                self.possible_action_states[state] = new_value
                return
        return
        
    # USED FOR UPDATING THE INTERPRETABLE STATE BASED ON WHICH ACTION IS DISPLAYED
    # updates a specified action or modifier to a new boolean value
    # UPDATING AN ACTION WILL SET ALL OTHER ACTIONS TO FALSE
    # UPDATING A MODIFIER WILL SET ALL OTHER MODIFIERS TO FALSE
    #
    # MODIFERS AND ACTIONS ARE ASSUMED TO BE MUTUALLY EXCLUSIVE WHEN UPDATING
    def update_actual_states(self, state_to_update, new_value):
        # modifier actions only effect other modifier actions        
        if state_to_update in self.actual_action_states['modifiers']:
            for modifier in self.actual_action_states['modifiers']:
                if state_to_update == modifier:
                    self.actual_action_states['modifiers'][modifier] = new_value
                    self.current_modifier = modifier
                else:
                    self.actual_action_states['modifiers'][modifier] = False
            if new_value == False:
                self.actual_action_states['modifiers'][self.default_modifier] = True
                self.current_modifier = self.default_modifier
            return

        # regular actions only effect other regular actions
        if state_to_update in self.actual_action_states['actions']:
            for action in self.actual_action_states['actions']:
                if action == state_to_update:
                    self.actual_action_states['actions'][action] = new_value
                    self.current_action = action
                else:
                    self.actual_action_states['actions'][action] = False
            if new_value == False:
                self.actual_action_states['actions'][self.default_action] = True
                self.current_action = self.default_action
            return
        return