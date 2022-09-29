import npc_greedy
import action_key_map
import affecter

rule_file = open('affect_rules/test_passions_rules.json', 'r')
rika_affecter = affecter.Affecter(rule_file)
rika_affect_vector = affecter.make_affect_vector(rika_affecter.affect_rules.keys(), rika_affecter.affect_rules)

# setup the input mapping
npc_key_map = {
                'actions': { 
                    'open_flow': [None], 
                    'closed_flow': [None], 
                    'projected_energy': [None]
                },
                'modifiers': {
                    'tempo_up': [None],
                    'tempo_down': [None]
                }
           }
npc_gesture_keys = action_key_map.Action_Key_Map(npc_key_map)

npc_brain = npc_greedy.Greedy_Search(len(npc_gesture_keys.actual_action_states['actions'].keys()), len(npc_gesture_keys.actual_action_states['modifiers'].keys()), rika_affect_vector.keys())

action, modifier = npc_brain.think(npc_gesture_keys, rika_affecter, rika_affect_vector, 'joy')

rika_affecter.update_affect(rika_affect_vector, action, modifier)

print()

print(npc_brain.think(npc_gesture_keys, rika_affecter, rika_affect_vector, 'joy'))

rika_affecter.update_affect(rika_affect_vector, action, modifier)

print()

print(npc_brain.think(npc_gesture_keys, rika_affecter, rika_affect_vector, 'sadness'))