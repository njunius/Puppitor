import affecter
import action_key_map

test_rule_file = open('affect_rules/test_passions_rules.json', 'r')
different_rule_file = open('affect_rules/test_different_rules.json', 'r')

test_affecter = affecter.Affecter(test_rule_file)
test_affect_vector = affecter.make_affect_vector(test_affecter.affect_rules.keys(), test_affecter.affect_rules)
print('test affecter:\n', test_affecter.affect_rules, test_affecter.equilibrium_action)
print()
print('test affect vector:\n', test_affect_vector)
print()

different_affecter = affecter.Affecter(different_rule_file, affect_floor = -2.0, affect_ceiling = 2.0, equilibrium_action = 'sit')
different_affect_vector = affecter.make_affect_vector(different_affecter.affect_rules.keys(), different_affecter.affect_rules)

print('different affecter:\n', different_affecter.affect_rules, different_affecter.floor_value, different_affecter.ceil_value, different_affecter.equilibrium_action)
print()
print('different affect vector:\n', different_affect_vector)
print()
print()

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
           
different_keymap = {
            'actions' : {
                'stand' : [None],
                'sit' : [None],
                'cross_legs' : [None],
                'cross_arms' : [None],
                'lean_forward' : [None]
            },
            'modifiers' : {
                'casually' : [None],
                'threateningly' : [None],
                'worriedly' : [None]
            }
           }

test_gesture_keys_obj = action_key_map.Action_Key_Map(keymap)
print()

different_gesture_keys_obj = action_key_map.Action_Key_Map(different_keymap, default_action = 'sulk', default_modifier = 'openly')
print()
print()

print('test output:\n')

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

print(affecter.get_possible_affects(test_affecter, test_affect_vector))
print(affecter.get_prevailing_affect(test_affecter, test_affect_vector))

print('\ndifferent output:\n')

different_gesture_keys_obj.update_possible_states('stand', True)
different_gesture_keys_obj.update_possible_states('sit', True)
different_gesture_keys_obj.update_possible_states('cross_legs', True)
different_gesture_keys_obj.update_possible_states('lean_forward', True)

print(different_gesture_keys_obj.possible_action_states)
print()

different_gesture_keys_obj.update_actual_states('stand', 'actions', True)
different_affecter.update_affect(different_affect_vector, different_gesture_keys_obj.current_states['actions'], different_gesture_keys_obj.current_states['modifiers'])
print(different_gesture_keys_obj.actual_action_states)
print()
print(different_affect_vector)
print()

different_gesture_keys_obj.update_actual_states('sit', 'actions', True)
different_affecter.update_affect(different_affect_vector, different_gesture_keys_obj.current_states['actions'], different_gesture_keys_obj.current_states['modifiers'])
print(different_gesture_keys_obj.actual_action_states)
print()
print(different_affect_vector)
print()

different_gesture_keys_obj.update_actual_states('cross_legs', 'actions', True)
different_affecter.update_affect(different_affect_vector, different_gesture_keys_obj.current_states['actions'], different_gesture_keys_obj.current_states['modifiers'])
print(different_gesture_keys_obj.actual_action_states)
print()
print(different_affect_vector)
print()

different_gesture_keys_obj.update_actual_states('lean_forward', 'actions', True)
different_affecter.update_affect(different_affect_vector, different_gesture_keys_obj.current_states['actions'], different_gesture_keys_obj.current_states['modifiers'])
print(different_gesture_keys_obj.actual_action_states)
print()
print(different_affect_vector)
print()

print(affecter.get_possible_affects(different_affecter, different_affect_vector))
print(affecter.get_prevailing_affect(different_affecter, different_affect_vector))
