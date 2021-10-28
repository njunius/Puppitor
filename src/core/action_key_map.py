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

class Action_Key_Map:
    
    def __init__(self, key_map, default_action = 'resting', default_modifier = 'neutral'):
        
        # ALL must have a value corresponding to a key in the actual_action_states dictionary of actions or modifiers
        # for the current usage both the current and default actions are initialized to the first value in the actions list 
        # for the current usage both the current and default modifiers are initialized to the last value in the modifiers list
        
        # this dictionary and values should not be modified ever and are generally for internal use only
        self._default_states = {
                                'actions' : default_action,
                                'modifiers' : default_modifier
                              }
        # this dictionary and values should only be modified internally and are used to access the current
        # state of the actions being performed 
        self.current_states = {
                                'actions' : self._default_states['actions'],
                                'modifiers' : self._default_states['modifiers']
                              }
        # example keymap
        # NOTE THAT THE KEYMAP SHOULD BE USING LISTS FOR KEYS TO ALLOW FOR THE POSSIBILITY OF MULTIPLE KEYS PERFORMING THE SAME ACTION
        """self.keymap = {
                            'actions': { 
                                'open_flow': [pygame.K_n], 
                                'closed_flow': [pygame.K_m], 
                                'projected_energy': [pygame.K_b]
                            },
                            'modifiers': {
                                'tempo_up': [pygame.K_c],
                                'tempo_down': [pygame.K_z]
                            }
                         }"""
        
        self.keymap = key_map
        
        print('\nkeymap:\n', self.keymap)
        
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
            
        for action in self.keymap['actions']:
            self.possible_action_states[action] = False
            
        for modifier in self.keymap['modifiers']:
            self.possible_action_states[modifier] = False
            
        print('\npossible action states:\n', self.possible_action_states)
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
                        # 'pause' : False # a cadence action
                      }"""
        self.actual_action_states = {
                                      'actions' : {},
                                      'modifiers' : {}
                                    }
        for category in self.actual_action_states:
            if category == 'actions':
                self.actual_action_states['actions'][default_action] = True
                for action in self.keymap['actions']:
                    self.actual_action_states['actions'][action] = False
            
            if category == 'modifiers':
                self.actual_action_states['modifiers'][default_modifier] = True
                for modifier in self.keymap['modifiers']:
                    self.actual_action_states['modifiers'][modifier] = False
                        
        print('\nactual action states:\n', self.actual_action_states)
        
        # allows toggling of keys rather than press and hold when true
        self.toggle = False
        
    # USED FOR UPDATING BASED ON KEYBOARD INPUTS
    # updates a specified state to a new boolean value
    def update_possible_states(self, state_to_update, new_value):
        if state_to_update in self.possible_action_states:
            self.possible_action_states[state_to_update] = new_value
        return
        
    # USED FOR UPDATING THE INTERPRETABLE STATE BASED ON WHICH ACTION IS DISPLAYED
    # updates a specified action or modifier to a new boolean value
    # UPDATING AN ACTION WILL SET ALL OTHER ACTIONS TO FALSE
    # UPDATING A MODIFIER WILL SET ALL OTHER MODIFIERS TO FALSE
    #
    # MODIFERS, ACTIONS, AND CADENCES ARE ASSUMED TO BE MUTUALLY EXCLUSIVE WHEN UPDATING
    def update_actual_states(self, state_to_update, class_of_action, new_value):
        
        if state_to_update in self.actual_action_states[class_of_action]:
            # go through each of the possible actions or modifiers or cadences
            # and set all but the one being explicitly changed to False
            # and use the given value (new_value) to update the value of the
            # specified action/modifier/cadence
            for state in self.actual_action_states[class_of_action]:
                if state_to_update == state:
                    self.actual_action_states[class_of_action][state] = new_value
                    self.current_states[class_of_action] = state
                else:
                    self.actual_action_states[class_of_action][state] = False
            if new_value == False:
                # return to doing the default behavior
                self.current_states[class_of_action] = self._default_states[class_of_action]
                self.actual_action_states[class_of_action][self._default_states[class_of_action]] = True
            return
        else:
            print('state: ' + state_to_update + ' is not a type of ' + class_of_action)
        return
        