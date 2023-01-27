import action_key_map
import affecter
import npc_a_star

def update_from_path(path):
    node = path.pop()
    action = node[1]
    modifier = node[2]
    
    return (action, modifier)
    
def maximize_minimize_affect_vector(affect_vector, char_affecter):
    count = 0
    for affect in character_av:
        if count % 2 == 0:
            character_av[affect] = 0.0
        else:
            character_av[affect] = 1.0
        
        count += 1
        
    affecter.get_prevailing_affect(char_affecter, affect_vector)
    return

def apply_print_path(path, character_av, step_value, verbose):
    while path:
        action, modifier = update_from_path(path)
        character_test.update_affect(character_av, action, modifier)
        
        if verbose:
            print('\naction and modifier: ' + action + ', ' + modifier)
            print('\ncharacter affect vector: ', character_av)
    return

def print_run_info(step_value, emotional_goal, affect_vector):
    print()
    print('\nstep value: ', step_value, '\nemotional goal: ', emotional_goal)
    print('\nstarting affect_vector: ', affect_vector, '\n')
    
    return

verbose = False

test_rule_file = open('affect_rules/test_passions_rules.json', 'r')
character_rule_file = open('affect_rules/rika_affect_rules.json', 'r')

test_affecter = affecter.Affecter(test_rule_file)
test_affect_vector = affecter.make_affect_vector(test_affecter.affect_rules.keys(), test_affecter.affect_rules)

character_test = affecter.Affecter(character_rule_file)
character_av = affecter.make_affect_vector(character_test.affect_rules.keys(), character_test.affect_rules)

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
         
test_actions = action_key_map.Action_Key_Map(keymap)

print()

# expected to return a path using Rika's ruleset
emotional_goal = 'anger'
step_value = 90
action = 'resting'
modifier = 'neutral'

print_run_info(step_value, emotional_goal, character_av)

action_path = []
start_node = (character_av, action, modifier, character_test.current_affect)
action_path = npc_a_star.npc_a_star_think(character_test, test_actions, start_node, emotional_goal, step_value)

apply_print_path(action_path, character_av, step_value, verbose)

print('\nfinal affect vector: ', character_av)
    
maximize_minimize_affect_vector(character_av, character_test)

# expected to return a path using Rika's ruleset        
emotional_goal = 'sadness'
action = 'resting'
modifier = 'neutral'

print_run_info(step_value, emotional_goal, character_av)

action_path = []
start_node = (character_av, action, modifier, character_test.current_affect)
action_path = npc_a_star.npc_a_star_think(character_test, test_actions, start_node, emotional_goal, step_value)

apply_print_path(action_path, character_av, step_value, verbose)

print('\nfinal affect vector: ', character_av)

maximize_minimize_affect_vector(character_av, character_test)

# expected to return a path using Rika's ruleset
emotional_goal = 'sadness'
action = 'resting'
modifier = 'neutral'
step_value = 30

print_run_info(step_value, emotional_goal, character_av)

action_path = []
start_node = (character_av, action, modifier, character_test.current_affect)
action_path = npc_a_star.npc_a_star_think(character_test, test_actions, start_node, emotional_goal, step_value)

apply_print_path(action_path, character_av, step_value, verbose)

print('\nfinal affect vector: ', character_av)

maximize_minimize_affect_vector(character_av, character_test)

# using Rika's ruleset this is expected to return NO PATH FOUND
emotional_goal = 'fear'
action = 'resting'
modifier = 'neutral'
step_value = 30

print_run_info(step_value, emotional_goal, character_av)

action_path = []
start_node = (character_av, action, modifier, character_test.current_affect)
action_path = npc_a_star.npc_a_star_think(character_test, test_actions, start_node, emotional_goal, step_value)

apply_print_path(action_path, character_av, step_value, verbose)

print('\nfinal affect vector: ', character_av)
