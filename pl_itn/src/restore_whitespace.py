import re
import string
from typing import List, Dict

punctuation = string.punctuation


class WhitespaceRestorer:
    def __init__(self, original: str, normalized: str, tokens: List[Dict]) -> None:
        """
        Finite State Transducers normalization loses record of the self.original whitespace.
        Each token of the self.normalized text is separated by a single space, no matter if there was no, single or multiple spaces in the given spot self.originally.
                `! (dwunasta)` -> `! ( 12 )`
        
        WhitespaceRestorer detects words which have not been transformed by the normalizer (mostly punctuation marks) and restores the self.original spaces around them.
                `! (dwunasta)` -> `! ( 12 )` -> `! (12)`
        
        Args:        
            self.original (str): Input phrase, for example "Jest godzina piętnasta trzydzieści."
            self.normalized (str): ITN output phrase, for example "Jest godzina 15:30 ."
            tokens ([dict]): parsed tokens from FST tagging, for example 
                `[OrderedDict([('tokens', OrderedDict([('name', 'jest')]))]), OrderedDict([('tokens', OrderedDict([('time', OrderedDict([('complement', 'godzina'), ('hours', '15'), ('minutes', '30')]))]))]), OrderedDict([('tokens', OrderedDict([('name', '.')]))])]`
        """
        lower_list = lambda x: [w.lower() for w in x]
        
        self.normalized = normalized.split(" ")
        self.normalized_lower = lower_list(self.normalized)
        
        self.original = re.split(fr"(\s+|[{punctuation}])", original) # ie. ['Jest', ' ', 'godzina', ' ', 'piętnasta', ' ', 'trzydzieści', '.']
        self.original = [w for w in self.original if len(w) > 0]
        self.original_lower = lower_list(self.original)
        
        self.tokens = tokens
    
    def run(self) -> str:
        restored = ""
        
        for token in self.tokens:
            token = token["tokens"] # OrderedDict([('tokens', OrderedDict([('name', 'jest')]))]) -> OrderedDict([('name', 'jest')])
            
            # Tokens tagged as `name` have not been transformed during FST normalization.
            # ie. `OrderedDict([('name', 'jest')])` or `OrderedDict([('name', '.')])`
            is_original_form = lambda x: x.get("name")
            
            if is_original_form(token):
                word = token["name"]

                # the word has not been transformed, so it can be found both in the self.normalized and self.original texts
                index_normalized = self.normalized_lower.index(word)
                index_original = self.original_lower.index(word)
                
                # if the word is preceded by transformed words in the self.normalized text, add them first
                restored += " ".join(self.normalized[:index_normalized])
                
                # compose a group of the word itself sorrounded by its self.original white spaces. Add it to the output.
                def maybe_get_whitespace(input_list, index):
                    try:
                        value = input_list[index]
                    except IndexError:
                        return ""
                    if re.match('^\s+$', value):
                        return value
                    return ""
                
                word_with_spaces = (
                    maybe_get_whitespace(self.original, index_original-1) +
                    self.original[index_original] +
                    maybe_get_whitespace(self.original, index_original+1)
                )
                restored += word_with_spaces
                
                if maybe_get_whitespace(self.original, index_original+1):
                    # Include trailing whitespace to the processed part
                    index_original += 1

                # Remove processed input
                def slice_head(input_list, index):
                    try:
                        output_list = input_list[index+1:]
                    except IndexError:
                        output_list = []
                    return output_list

                self.normalized = slice_head(self.normalized, index_normalized)
                self.normalized_lower = slice_head(self.normalized_lower, index_normalized)
                self.original = slice_head(self.original, index_original)
                self.original_lower = slice_head(self.original_lower, index_original)
         
        restored += " ".join(self.normalized)
        return restored