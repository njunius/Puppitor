import npc_greedy
import action_key_map
import affecter

rule_file = open('affect_rules/rika_affect_rules.json', 'r')
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
# and applied by the punctuation_printout_rules module
npc_gesture_keys = action_key_map.Action_Key_Map(npc_key_map)

action, modifier = npc_greedy.think(npc_gesture_keys, rika_affecter, rika_affect_vector, 'joy')

rika_affecter.update_affect(rika_affect_vector, action, modifier)

print()

npc_greedy.think(npc_gesture_keys, rika_affecter, rika_affect_vector, 'joy')

rika_affecter.update_affect(rika_affect_vector, action, modifier)

print()

npc_greedy.think(npc_gesture_keys, rika_affecter, rika_affect_vector, 'joy')