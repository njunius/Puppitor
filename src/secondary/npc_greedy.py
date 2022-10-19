import action_key_map
import affecter
import copy

class Greedy_Search:

    # creates object pools of future states and state copies based on the number of actions and modifiers of the Puppitor domain being used
    def __init__(self, num_actions, num_modifiers, affects_list):
        # object pool of states that will be evaluated (list of goal value, action, modifier)
        self.future_states_for_evaluation = []
        for i in range(0, num_actions * num_modifiers):
            self.future_states_for_evaluation.append((0.0, '', ''))
        
        # object pool of affect vector copies (list of dictionaries)
        self.copied_states = []
        for i in range(0, num_actions * num_modifiers):
            self.copied_states.append({})
            for affect in affects_list:
                self.copied_states[i][affect] = 0.0
                
        self.goal_emotion_value = 0.0
        self.simulation_index = 0

    def think(self, action_key_map, character_affecter, current_emotional_state, goal_emotion):
        self.goal_emotion_value = 0.0
        self.simulation_index = 0
        
        #for action in action_key_map.actual_action_states['actions'].keys():
        #    for modifier in action_key_map.actual_action_states['modifiers'].keys():
        for action_modifier_pair in action_key_map.moves:
            #print(action, modifier)
            action, modifier = action_modifier_pair
            self.copied_states[self.simulation_index] = current_emotional_state.copy() # copy.deepcopy(current_emotional_state)
            character_affecter.update_affect(self.copied_states[self.simulation_index], action, modifier)
            #print(copied_state.affects)
            
            self.goal_emotion_value = self.copied_states[self.simulation_index][goal_emotion]
            #print(goal_emotion, goal_emotion_value)
            self.future_states_for_evaluation[self.simulation_index] = (affecter.evaluate_affect_vector(character_affecter, self.copied_states[self.simulation_index], goal_emotion), action, modifier)
            
            self.simulation_index += 1
                
        sorted_states = sorted(self.future_states_for_evaluation, key=lambda state: state[0], reverse = True) # sort by goal emotion value
        #print(sorted_states)
        emotional_value, best_action, best_modifier = sorted_states[0]
        #print(emotional_value, best_action, best_modifier)
            
        return (best_action, best_modifier)