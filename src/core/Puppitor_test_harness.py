import affecter
import gesture_keys
import animation_structure

test_rule_file = open('affect_rules/test_passions_rules.json', 'r')

test_affecter = affecter.Gesture_Affecter(test_rule_file)
test_anim_struct = animation_structure.Animation_Structure(4)
test_affect_vector = affecter.make_affect_vector(test_affecter.affect_rules.keys(), test_affecter.affect_rules)

keymap = {
                'actions': { 
                    'open_flow': ['pygame.K_n'], 
                    'closed_flow': ['pygame.K_m'], 
                    'projected_energy': ['pygame.K_b']
                },
                'modifiers': {
                    'tempo_up': ['pygame.K_c'],
                    'tempo_down': ['pygame.K_z']
                }
           }

test_gesture_keys_obj = gesture_keys.Gesture_Interface(keymap)

test_gesture_keys_obj.update_possible_states('open_flow', True)
test_gesture_keys_obj.update_possible_states('tempo_up', True)
test_gesture_keys_obj.update_possible_states('tempo_down', True)
test_gesture_keys_obj.update_possible_states('closed_flow', True)
test_gesture_keys_obj.update_possible_states('projected_energy', True)
test_gesture_keys_obj.update_possible_states('pause', True)

print(test_gesture_keys_obj.possible_action_states)
print()

test_gesture_keys_obj.update_actual_states('open_flow', 'actions', True)
test_affecter.update_affect(test_affect_vector, test_gesture_keys_obj.current_states['actions'], test_gesture_keys_obj.current_states['modifiers'])
print(test_gesture_keys_obj.actual_action_states)
print()
print(test_affect_vector)
test_gesture_keys_obj.update_actual_states('closed_flow', 'actions', True)
test_affecter.update_affect(test_affect_vector, test_gesture_keys_obj.current_states['actions'], test_gesture_keys_obj.current_states['modifiers'])
print(test_gesture_keys_obj.actual_action_states)
print()
print(test_affect_vector)
print()
test_gesture_keys_obj.update_actual_states('projected_energy', 'actions', True)
test_affecter.update_affect(test_affect_vector, test_gesture_keys_obj.current_states['actions'], test_gesture_keys_obj.current_states['modifiers'])
print(test_gesture_keys_obj.actual_action_states)
print()
print(test_affect_vector)
print()
test_gesture_keys_obj.update_actual_states('resting', 'actions', True)
test_affecter.update_affect(test_affect_vector, test_gesture_keys_obj.current_states['actions'], test_gesture_keys_obj.current_states['modifiers'])
print(test_gesture_keys_obj.actual_action_states)
print()
print(test_affect_vector)
print()
test_gesture_keys_obj.update_actual_states('tempo_up', 'modifiers', True)
test_affecter.update_affect(test_affect_vector, test_gesture_keys_obj.current_states['actions'], test_gesture_keys_obj.current_states['modifiers'])
print(test_gesture_keys_obj.actual_action_states)
print()
print(test_affect_vector)
print()
test_gesture_keys_obj.update_actual_states('tempo_down', 'modifiers', True)
test_affecter.update_affect(test_affect_vector, test_gesture_keys_obj.current_states['actions'], test_gesture_keys_obj.current_states['modifiers'])
print(test_gesture_keys_obj.actual_action_states)
print()
print(test_affect_vector)
print()
test_gesture_keys_obj.update_actual_states('neutral', 'modifiers', True)
test_affecter.update_affect(test_affect_vector, test_gesture_keys_obj.current_states['actions'], test_gesture_keys_obj.current_states['modifiers'])
print(test_gesture_keys_obj.actual_action_states)
print()
print(test_affect_vector)
print()

print(test_affecter.get_possible_affects(test_affect_vector))
print(test_affecter.get_prevailing_affect(test_affect_vector))