import sys
import json
import action_key_map
import affecter
import npc_a_star
import test_helper as th

# runs a unit test of a given rule file and key map
# loops through each available affect setting the goal affect value to 0 and all other affect values to 1
# prints the run information of each trial or no path found for a given trial
# arguments:
#   rule file path (string)
#   key map file path (string)
#   default action (string)
#   default modifier (string)
#   step multiplier (number)
#   verbose flag (boolean)
#   optional queue size (number)
def main():
    verbose = False
    default_action = ''
    default_modifier = ''
    queue_limit = 18000

    args = sys.argv[1:]
    if not args or len(args) < 6:
        print('USAGE: <rule file path> <key map file path> <default action string> <default modifier string> <step multiplier value> <verbose flag F or T> <optional queue size limit>\nEXITING WITH RETURN VALUE 2')
        return 2
    
    rule_file_path = args[0]
    key_map_file_path = args[1]
    default_action = args[2]
    default_modifier = args[3]
    step_value = float(args[4])
    if args[5] == 'f' or args[5] == 'F':
        verbose = False
    elif args[5] == 't' or args[5] == 'T':
        verbose = True
    else:
        print('args[3] EXPECTED VALUE EITHER \'F\' or \'T\' EXITING WITH RETURN VALUE 2')
        return 2
    
    if len(args) == 7:
        queue_limit = int(args[6])

    test_rule_file = open(rule_file_path, 'r')

    character_test = affecter.Affecter(test_rule_file)
    character_av = affecter.make_affect_vector(character_test.affect_rules.keys(), character_test.affect_rules)

    key_file = open(key_map_file_path, 'r')
    keymap = json.load(key_file)
    
    test_actions = action_key_map.Action_Key_Map(keymap, default_action, default_modifier)

    print()
    
    for affect in character_av:
        emotional_goal = affect
        action = test_actions._default_states['actions']
        modifier = test_actions._default_states['modifiers']
        
        th.maximize_minimize_affect_vector(character_av, character_test, affect)
        
        th.print_run_info(step_value, emotional_goal, character_av)
        
        action_path = []
        start_node = (character_av, action, modifier, character_test.current_affect)
        action_path = npc_a_star.npc_a_star_think(character_test, test_actions, start_node, emotional_goal, step_value, queue_limit)

        th.apply_print_path(action_path, character_test, character_av, step_value, verbose)
        
        print('\nfinal affect vector: ', character_av)
    
    return 0
    
if __name__ == '__main__':
    sys.exit(main())
    