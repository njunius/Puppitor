import sys
import json
import action_key_map
import affecter
import npc_a_star

def update_from_path(path):
    node = path.pop()
    action = node[1]
    modifier = node[2]
    
    return (action, modifier)
    
def maximize_minimize_affect_vector(affect_vector, char_affecter, goal_emotion):
    for affect in affect_vector:
        if affect == goal_emotion:
            affect_vector[affect] = 0
        else:
            affect_vector[affect] = 1
        
    affecter.get_prevailing_affect(char_affecter, affect_vector)
    return

def apply_print_path(path, char_affecter, character_av, step_value, verbose):
    while path:
        action, modifier = update_from_path(path)
        char_affecter.update_affect(character_av, action, modifier)
        
        if verbose:
            print('\naction and modifier: ' + action + ', ' + modifier)
            print('\ncharacter affect vector: ', character_av)
    return

def print_run_info(step_value, emotional_goal, affect_vector):
    print()
    print('\nstep value: ', step_value, '\nemotional goal: ', emotional_goal)
    print('\nstarting affect_vector: ', affect_vector, '\n')
    
    return

# runs a unit test of a given rule file and key map
# loops through each available affect setting the goal affect value to 0 and all other affect values to 1
# prints the run information of each trial or no path found for a given trial
# arguments:
#   rule file path (string)
#   key map file path (string)
#   step multiplier (number)
#   verbose flag (boolean)
#   default action (string)
#   default modifier (string)
def main():
    verbose = False
    default_action = ''
    default_modifier = ''

    args = sys.argv[1:]
    if not args or len(args) != 6:
        print('USAGE: <rule file path> <key map file path> <default action string> <default modifier string> <step multiplier value> <verbose flag F or T>\nEXITING WITH RETURN VALUE 2')
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

    test_rule_file = open(rule_file_path, 'r')

    character_test = affecter.Affecter(test_rule_file)
    character_av = affecter.make_affect_vector(character_test.affect_rules.keys(), character_test.affect_rules)

    key_file = open(key_map_file_path, 'r')

    '''keymap = {
                'actions': { 
                    'open_flow': ['pygame.K_n'], 
                    'closed_flow': ['pygame.K_m'], 
                    'projected_energy': ['pygame.K_b']
                },
                'modifiers': {
                    'tempo_up': ['pygame.K_c'],
                    'tempo_down': ['pygame.K_z']
                }
             }'''
    keymap = json.load(key_file)
    
    test_actions = action_key_map.Action_Key_Map(keymap, default_action, default_modifier)

    print()
    
    for affect in character_av:
        emotional_goal = affect
        action = test_actions._default_states['actions']
        modifier = test_actions._default_states['modifiers']
        
        maximize_minimize_affect_vector(character_av, character_test, affect)
        
        print_run_info(step_value, emotional_goal, character_av)
        
        action_path = []
        start_node = (character_av, action, modifier, character_test.current_affect)
        action_path = npc_a_star.npc_a_star_think(character_test, test_actions, start_node, emotional_goal, step_value)

        apply_print_path(action_path, character_test, character_av, step_value, verbose)
        
        print('\nfinal affect vector: ', character_av)
    
    return 0
    
if __name__ == '__main__':
    sys.exit(main())
    