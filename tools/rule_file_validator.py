import sys
import json
import csv
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
    start_node = (character_av, action, modifier, affecter.get_prevailing_affect(character_test, character_av))
    action_path = npc_a_star.npc_a_star_think(character_test, test_actions, start_node, goal_emotion, step_value, queue_limit, analysis = True)

    if not action_path:
        print('NO PATH FOUND')
        return 0
    
    response_curve = []
    if len(action_path) > 1:
        response_curve = th.find_all_affect_changes(action_path)
    else:
        response_curve.append(th.delta_info._make((0, action_path[0][3], action_path[0][3], action_path[0][3], action_path[0][1], action_path[0][2])))
    with open('response_curve.csv', 'w', newline = '') as csvfile:
        response_writer = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
        
        print(action_path[-1])
        
        start_state, start_action, start_mod, start_affect = action_path[len(action_path) - 1]
        
        response_writer.writerow(['count', 'init_affect', 'prev_affect', 'curr_affect', 'curr_action', 'curr_modifier'])
        if len(response_curve) > 1:
            response_writer.writerow([0, start_affect, start_affect, start_affect, start_action, start_mod]) # add initial state to file
    
        affect_step_cache = 0
    
        for i, node in enumerate(response_curve):
            step_diff = node.count
            if i > 0:
                step_diff = node.count - response_curve[i - 1].count
                
            if node.prev_affect != node.curr_affect:
                if affect_step_cache == 0:
                    step_diff = node.count
                else:
                    step_diff = node.count - affect_step_cache
                
                print('\nnumber of steps to display a new affect: ', step_diff, '\nprevious affect: ', node.prev_affect, '\nnew affect: ', node.curr_affect, '\nit will take ', step_diff / 60, ' seconds for the player to see a new expression in a 60hz update loop', '\naction: ', node.curr_action, '\nmodifier: ', node.curr_mod)
                affect_step_cache = node.count
            else:
                print('\nnumber of steps for a new action or modifier to be used: ', step_diff, '\naction: ', node.curr_action, '\nmodifier: ', node.curr_mod)
            
            response_writer.writerow([node.count, node.init_affect, node.prev_affect, node.curr_affect, node.curr_action, node.curr_mod])
        
        end = response_curve[-1]
        response_writer.writerow([len(action_path), end.init_affect, end.curr_affect, end.curr_affect, end.curr_action, end.curr_mod]) # add the last step to the file
            
    th.apply_print_path(action_path, character_test, character_av, step_value, verbose)    
    print('\nfinal affect vector: ', character_av)

    return 0
    

if __name__ == '__main__':
    sys.exit(main())
    