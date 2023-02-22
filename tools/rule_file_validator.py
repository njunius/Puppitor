import sys
import json
import action_key_map
import affecter
import npc_a_star
import test_helper as th

# runs a test of a given rule file, key map, starting affect vector and goal emotion
# runs an A* search from an affect vector to a state that expresses the goal emotion
# prints the run information of the trial or no path found if the queue size limit was reached
# arguments:
#   rule file path (string)
#   key map file path (string)
#   affect vector file path (string)
#   goal emotion (string)
#   default action (string)
#   default modifier (string)
#   step multiplier (number)
#   verbose flag (boolean)
#   optional queue size limit
def main():
    verbose = False
    default_action = ''
    default_modifier = ''
    queue_limit = 18000

    args = sys.argv[1:]
    if not args or len(args) < 8:
        print('USAGE: <rule file path> <key map file path> <affect vector file> <goal emotion> <default action string> <default modifier string> <step multiplier value> <verbose flag F or T> <optional queue size limit>\nEXITING WITH RETURN VALUE 2')
        return 2
    
    rule_file_path = args[0]
    key_map_file_path = args[1]
    affect_vector_file_path = args[2]
    goal_emotion = args[3]
    default_action = args[4]
    default_modifier = args[5]
    step_value = float(args[6])
    if args[7] == 'f' or args[7] == 'F':
        verbose = False
    elif args[7] == 't' or args[7] == 'T':
        verbose = True
    else:
        print('args[3] EXPECTED VALUE EITHER \'F\' or \'T\' EXITING WITH RETURN VALUE 2')
        return 2
    
    if len(args) == 9:
        queue_limit = int(args[8])

    test_rule_file = open(rule_file_path, 'r')

    character_test = affecter.Affecter(test_rule_file)
    
    test_av_file = open(affect_vector_file_path, 'r')
    character_av = json.load(test_av_file)

    key_file = open(key_map_file_path, 'r')
    keymap = json.load(key_file)
    
    test_actions = action_key_map.Action_Key_Map(keymap, default_action, default_modifier)

    print()

    action = test_actions._default_states['actions']
    modifier = test_actions._default_states['modifiers']
        
    th.print_run_info(step_value, goal_emotion, character_av)
    
    action_path = []
    start_node = (character_av, action, modifier, character_test.current_affect)
    action_path = npc_a_star.npc_a_star_think(character_test, test_actions, start_node, goal_emotion, step_value, queue_limit)

    delta_node_info = th.find_first_affect_change(action_path)

    th.apply_print_path(action_path, character_test, character_av, step_value, verbose)
    
    print('\nnumber of steps to display a new affect: ', delta_node_info[0], '\ninitial affect: ', delta_node_info[1], '\nnew affect: ', delta_node_info[2])
    
    print('\nif in a 60hz update loop it will take ', delta_node_info[0] / 60, ' seconds for a player to see a new expression')
    
    print('\nfinal affect vector: ', character_av)

    return 0
    

if __name__ == '__main__':
    sys.exit(main())
    