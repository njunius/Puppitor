import sys
import json
import random
import argparse

def main():

    parser = argparse.ArgumentParser(prog = 'Puppitor Rule File Generator',
                                     description = 'Generates a new rule file based on the template provided')
    
    parser.add_argument('-t', '--template_file_path', default = './affect_rules/test_passions_rules.json', help = 'the path and to the character rule file. must include file name and extension')
    parser.add_argument('-o', '--output_file_path', default = './affect_rules/new_random_rule.json', help = 'the path to the output file. must include file name and extension')

    args = parser.parse_args()
    
    template_path = args.template_file_path
    output_path = args.output_file_path

    rule_file = open(template_path, 'r')

    rfs = json.load(rule_file)

    print('\ntemplate rule file: \n', rfs, '\n')

    affects = list(rfs.keys())

    for affect in affects:
        curr_affect = rfs[affect]
        
        # randomize each individual action and modifier value of the current affect entry
        for action in list(curr_affect['actions'].keys()):
            curr_affect['actions'][action] = random.uniform(-0.01, 0.01)
        
        for modifier in list(curr_affect['modifiers'].keys()):
            curr_affect['modifiers'][modifier] = random.uniform(-0.01, 0.01)
            
        # randomize the equilibrium point of the current affect
        curr_affect['equilibrium_point'] = random.random()
        
        # setup randomized adjacencies
        len_adj = random.randint(0, len(affects))
        adj_affects = random.sample(affects, len_adj)
        
        # make uniform weighting of adjacent affects
        if len_adj > 0:
            adj_dict = {}
            value = 100 // len_adj
            
            # since we are doing integer math and adjacencies must add up to 100, take the difference between the results of the division for use later
            diff = 100 - (value * len_adj)
            
            for affect in adj_affects:
                value = 100 // len_adj
                adj_dict[affect] = value
            
            # re-add the difference between the sum of the adjacency weights and 100
            adj_dict[adj_affects[0]] += diff
            
            curr_affect['adjacent_affects'] = adj_dict
            
        
    print('randomized rule file: \n', rfs, '\n')

    new_rule_file = open(output_path, 'w')

    json.dump(rfs, new_rule_file, indent = 4)
    
    print('file written to: ' + output_path)
    
    return 0
    
if __name__ == '__main__':
    sys.exit(main())