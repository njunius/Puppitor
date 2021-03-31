#
# Punctuation_Printout_Rules is a wrapper around a JSON object mapping punctuation to user defined tags
# the primary function of this class is to insert semantic tags into arbitrary strings and is primarily
# intended for use with Ren'Py but any consistent set of tags can be used
#
import json

class Punctuation_Printout_Rules:
    def __init__(self, punctuation_rules_file):
        # load the opened specified punctuation rule file
        # punctuation rules are organized as [punctuation] as keys and [semantic tag] as values 
        self.punctuation_rules = json.load(punctuation_rules_file)
                    
        self.num_insertions = 0
        
        print(self.punctuation_rules.keys())
           
    # thank you to Max Kreminski for hammering out a tokenizer and emitter for fun that I could then go and butcher
    
    # breaks up an input_str into plain text 'PLAIN' and semantically relevant text 'SPECIAL' stored as a list of tokens of tuples of (<TOKEN TYPE>, <TOKEN STRING>)
    def tokenize(self, input_str):
        specials = sorted(self.punctuation_rules.keys(), key=len, reverse=True) # so the longest ones get first pass at matching
        index = 0
        tokens = []
        curr_plain_str = ''
        self.num_insertions = 0
        while index < len(input_str):
            # go through the input string and if we see a character or string that is in the insert rules we say we have found a new special
            matching_special = next((curr_spec for curr_spec in specials if input_str[index:index+len(curr_spec)] == curr_spec), None)
            # added a check to see if the matching_special is the last character in the line so there are not extraneous pauses at the end of printing lines
            if matching_special and index + len(matching_special) < len(input_str) - 1:
                # append curr_plain_str token to tokens first (and start a new curr_plain_str)
                # note: we do this unconditionally, so we emit garbage PLAIN empty string tokens between two specials
                # (but it shouldn't matter for our current usecase)
                tokens.append(('PLAIN', curr_plain_str))
                curr_plain_str = ''
                # then append the special we just found
                tokens.append(('SPECIAL', matching_special))
                index += len(matching_special)
                self.num_insertions += 1
            else:
                # add current character to curr_str
                curr_plain_str += input_str[index]
                index += 1
        # and append the trailing curr_plain_str token to tokens to close it out
        # note: this is again unconditional, same issue as above
        tokens.append(('PLAIN', curr_plain_str))
        return tokens

    # take a list of tokens of tuples, of type (<TOKEN TYPE>, <TOKEN STRING>) and output the full string
    # inserting the string markup associated with each of the SPECIAL tokens
    def emit(self, tokens, markup):
        out_str = ''
        for (token_type, token_text) in tokens:
            if token_type == 'PLAIN':
                out_str += token_text
            elif token_type == 'SPECIAL':
                out_str += token_text + markup[token_text]
            else:
                print('bad token type: ' + token_type)
        return out_str
    
    # wrapper around the tokenizer and emitter written by Max Kreminski to allow for simpler
    # application of rules in external programs though tokenize() and emit() can be used separately if desired
    def apply_rules(self, given_string):        
        tokens = self.tokenize(given_string)
        result_string = self.emit(tokens, self.punctuation_rules)
        
        return result_string
        