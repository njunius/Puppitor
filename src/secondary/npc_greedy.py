import action_key_map
import affecter
import copy

def think(action_key_map, character_affecter, current_emotional_state, goal_emotion):
    future_states_for_evaluation = []
    for action in action_key_map.actual_action_states['actions'].keys():
        for modifier in action_key_map.actual_action_states['modifiers'].keys():
            #print(action, modifier)
            copied_state = copy.deepcopy(current_emotional_state)
            character_affecter.update_affect(copied_state, action, modifier)
            #print(copied_state.affects)
            goal_emotion_value = copied_state[goal_emotion]
            #print(goal_emotion, goal_emotion_value)
            future_states_for_evaluation.append((goal_emotion_value, action, modifier))
            
    sorted_states = sorted(future_states_for_evaluation, key=lambda state: state[0], reverse = True) # sort by goal emotion value
    #print(sorted_states)
    emotional_value, best_action, best_modifier = sorted_states[0]
    #print(emotional_value, best_action, best_modifier)
        
    return (best_action, best_modifier)