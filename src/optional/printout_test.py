import punctuation_printout_rules

f = open('printout_rules/wait_insert_rules.json', 'r')

npc_print_rules = punctuation_printout_rules.Punctuation_Printout_Rules(f)

print(npc_print_rules.punctuation_rules)

line = 'your text, can go here to test- rules...'

print(npc_print_rules.apply_rules(line))

line = 'vary your punctuation in the rule files to test this.'

print(npc_print_rules.apply_rules(line))

line = 'you should notice that insertions do not happen when punctuation is at the end of the line.'

print(npc_print_rules.apply_rules(line))