import sys
import json
import csv
import argparse
import action_key_map
import affecter
import npc_a_star
import npc_greedy
import npc_uct
import test_helper as th

# runs a test of a given rule file, key map, starting affect vector and goal emotion
# runs an A* search from an affect vector to a state that expresses the goal emotion
# prints the run information of the trial or no path found if the queue size limit was reached
# arguments:
#   rule file path (path and filename of the Puppitor rule file)
#   key map file path (path and filename of the Puppitor key map)
#   affect vector file path (path and filename of the Puppitor affect vector)
#   goal emotion (name of the target affect to search for, must be present in Puppitor)
#   default action (name of the default Puppitor action)
#   default modifier (name of the default Puppitor modifier)
#   step value (how large a move the search is allowed to make)
# optional arguments:
#   -v, --verbose (sets the verbose path printing flag)
#   -q, --queue_limit (specifies a maximum queue allowance for A* search)
#   -i, --itermax (specifies the maximum iteration allowance for MCTS search)
#   -r, --rollmax (specifies the maximum rollout depth allowance for MCTS search)
#   -o, --output_file (specifies the name of the CSV file to be written)
def main():
    
    greedy_instance = None

    # set arguments
    parser = argparse.ArgumentParser(prog = 'Puppitor Rule File Evaluation Utility',
                                     description = 'Runs a search of the specified type over a desired affect vector using a chosen set of Puppitor actions and character rules')

    parser.add_argument('rule_file_path', default = './affect_rules/test_passions_rules.json', help = 'the path to the character rule file. must include file name and extension')
    parser.add_argument('key_map_path', default = './key_map.json', help = 'the path to the file containing the key map. must include file name and extension')
    parser.add_argument('av_file_path', default = './affect_vector.json', help = 'the path to the affect vector file. must include file name and extension')
    parser.add_argument('goal_emotion', default =  'fear', help = 'must be an affect that appears in the chosen affect vector and rule file')
    parser.add_argument('default_action', default = 'resting', help = 'must be an action that appears in the chosen rule file')
    parser.add_argument('default_modifier', default = 'neutral', help = 'must be a modifier that appears in the chosen rule file')
    parser.add_argument('step_value', type = int, default = 180, help = 'must be an integer value greater than 0')
    parser.add_argument('ai_mode', type = int, default = 0, choices=[0, 1, 2], metavar = 'ai_mode', help = 'selects which AI search to run. 0 selects A* search. 1 selects greedy search. 2 selects MCTS')
    parser.add_argument('-v', '--verbose', action = 'store_true', help = 'if set, the program will print the full path to the console')
    parser.add_argument('-q', '--queue_limit', nargs = '?', type = int, default = 18000, help = 'sets the queue limit for A* search')
    parser.add_argument('-i', '--itermax', nargs = '?', type = int, default = 2000, help = 'sets the maximum iteration limit of MCTS')
    parser.add_argument('-r', '--rollmax', nargs = '?', type = int, default = 50, help = 'sets the maximum limit for the rollout depth of MCTS')
    parser.add_argument('-o', '--output_file', nargs = '?', default = 'response_curve.csv', help = 'the name of the csv file to write to')

    args = parser.parse_args()

    # process positional arguments
    rule_file_path = args.rule_file_path
    affect_vector_file_path = args.av_file_path
    key_map_file_path = args.key_map_path
    goal_emotion = args.goal_emotion
    default_action = args.default_action
    default_modifier = args.default_modifier
    step_value = args.step_value
    ai_mode = args.ai_mode

    # process optional arguments
    verbose = args.verbose
    queue_limit = args.queue_limit
    itermax = args.itermax
    rollmax = args.rollmax
    output_file = args.output_file


    # setup Puppitor 
    test_rule_file = open(rule_file_path, 'r')

    character_test = affecter.Affecter(test_rule_file)
    
    test_av_file = open(affect_vector_file_path, 'r')
    character_av = json.load(test_av_file)

    key_file = open(key_map_file_path, 'r')
    keymap = json.load(key_file)
    
    test_actions = action_key_map.Action_Key_Map(keymap, default_action, default_modifier)

    # confirm no problems in arguments

    # first Puppitor domain entry
    first_key = list(character_test.affect_rules)[0]
    first_item = character_test.affect_rules[first_key]
    print('\nfirst item: ', first_item)

    if default_action not in first_item['actions']:
        print('\nDEFAULT ACTION NOT IN PUPPITOR DOMAIN\n\nCHECK WHICH FILES YOU ARE LOADING')
        return 2

    if default_modifier not in first_item['modifiers']:
        print('\nDEFAULT MODIFIER NOT IN PUPPITOR DOMAIN\n\nCHECK WHICH FILES YOU ARE LOADING')
        return 2

    if goal_emotion not in character_av or goal_emotion not in character_test.affect_rules.keys():
        print('\nGOAL EMOTION NOT IN PUPPITOR DOMAIN\n\nCHECK WHICH FILES YOU ARE LOADING')
        return 2

    if ai_mode == 1:
        p_states = test_actions.prevailing_states
        greedy_instance = npc_greedy.Greedy_Search(len(p_states['actions'].keys()), len(p_states['modifiers'].keys()), character_av.keys())
        print('\ngreedy instance created!\n', greedy_instance, '\n')

    action = test_actions._default_states['actions']
    modifier = test_actions._default_states['modifiers']
        
    th.print_run_info(step_value, goal_emotion, character_av)
    
    action_path = []
    start_node = (character_av, action, modifier, affecter.get_prevailing_affect(character_test, character_av))
    
    if ai_mode == 0:
        action_path = npc_a_star.npc_a_star_think(character_test, test_actions, start_node, goal_emotion, step_value, queue_limit, analysis = True)
    elif ai_mode == 1:        
        action_path = th.make_greedy_path(start_node, greedy_instance, test_actions, character_test, goal_emotion, step_value)
    elif ai_mode == 2:    
        action_path = th.make_mcts_path(start_node, npc_uct.uct_think, test_actions, character_test, goal_emotion, step_value, itermax, rollmax)

    if not action_path:
        print('NO PATH FOUND')
        return 0

    if ai_mode != 0:
        print('\npath length: ', len(action_path), '\n')
        
    response_curve = []
    if len(action_path) > 1:
        response_curve = th.find_all_affect_changes(action_path)
    else:
        response_curve.append(th.delta_info._make((0, action_path[0][3], action_path[0][3], action_path[0][3], action_path[0][1], action_path[0][2])))
        
    with open(output_file, 'w', newline = '') as csvfile:
        response_writer = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
        
        start_state, start_action, start_mod, start_affect = action_path[0]
        
        response_writer.writerow(['count', 'init_affect', 'prev_affect', 'curr_affect', 'curr_action', 'curr_modifier'])

        if len(response_curve) > 1: 
            response_writer.writerow([0, start_affect, start_affect, start_affect, start_action,start_mod]) # add initial state to file
    
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
    
    # prints the full path if in verbose mode
    if verbose:
        th.verbose_print(action_path)    
    print('\nfinal affect vector: ', action_path[-1][0]) # get the last node's affect vector

    return 0
    

if __name__ == '__main__':
    sys.exit(main())
    