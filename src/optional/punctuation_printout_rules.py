#
# Punctuation_Printout_Rules is a wrapper around a JSON object mapping punctuation to user defined tags
# the primary function of this class is to insert semantic tags into arbitrary strings and is primarily
# intended for use with Ren'Py but any consistent set of tags can be used
#
import json

class Punctuation_Printout_Rules:
    def __init__(self, punctuation_rules_name, punctuation_rules_directory):
        # load the specified punctuation rule file
        with open(punctuation_rules_directory + punctuation_rules_name) as entry:
            # punctuation rules are organized as [punctuation] as keys and [semantic tag] as values 
            self.punctuation_rules = json.load(entry)
            
        self.multi_character_punctuation = []
        
        for punctuation in self.punctuation_rules.keys():
            if len(punctuation) > 1:
                self.multi_character_punctuation.append(punctuation)
        
        self.num_insertions = 0
        
        print(self.punctuation_rules.keys())
        print(self.multi_character_punctuation)
           
           
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
            if matching_special:
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
    
    # takes a string and inserts semantic tags after each type of punctuation tracked by the rules
    # file stored in self.punctuation_rules
    # returns a new string with the semantic rules added after the punctuation they are associated with
    """def apply_rules(self, given_string):
        result_string = ''
        str_len = len(given_string)
        index = 0
        single_punct_skip_count = 0
        while index < str_len:        
            character = given_string[index]
            
            if self.multi_character_punctuation:
                # check if the character we are looking at could be a part of a multi-character punctuation
                for punctuation in self.multi_character_punctuation:
                    pnct_length = len(punctuation)
                    
                    # try the next multi-character piece of punctuation if we are not comparing the correct one
                    if character not in punctuation:
                        single_punct_skip_count += 1
                        continue
                    else:
                        if index <= str_len - pnct_length:
                            # use index + len(punctuation) - 1 because index is the first element in a multi-character punctuation
                            # if we are not actually looking at a multi-character piece of punctuation
                            # because what would be its final character does not match, just add the character
                            if given_string[index + pnct_length - 1] not in punctuation:
                                result_string += character + self.punctuation_rules[character]
                            else:
                                while index < str_len and given_string[index] in punctuation:
                                    index += 1
                                result_string += punctuation + self.punctuation_rules[punctuation]
                                index -= 1 # the outermost while loop will overshoot the next character by 1 so we need to reset it
                
                # if we were actually looking at a piece of single character punctuation
                if single_punct_skip_count == len(self.multi_character_punctuation) and character in self.punctuation_rules:
                    result_string += character + self.punctuation_rules[character]
                # or were not looking at a piece of punctuation at all
                elif character not in self.punctuation_rules:
                    char_in_punct = False
                    # make sure we aren't adding a redundant part of the multi-character punctuation
                    for multi_char_punct in self.multi_character_punctuation:
                        if character in multi_char_punct:
                            char_in_punct = True
                            break                    
                    if not char_in_punct:
                        result_string += character
                
                single_punct_skip_count = 0
                                    
            else:
                if character in self.punctuation_rules:
                    result_string += character + self.punctuation_rules[character]
                else:
                    result_string += character
            
            index += 1
        return result_string"""
            