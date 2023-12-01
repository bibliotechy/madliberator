from collections import Counter
from enum import Enum
from math import ceil
from random import choices
from sys import stdin

import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize.treebank import TreebankWordDetokenizer

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')
nltk.download('wordnet')

class WordType(Enum):
    NOUN = "NOUN"
    VERB = "VERB"
    ADJ  = "ADJ"
    ADV  = "ADV"

    PLURAL_NOUN = "PLURAL NOUN"

WNL = WordNetLemmatizer()

def space_token(word_type: WordType):
    return f"{{{{{word_type.name}}}}}"


class Mabliberator():

    stop_word_defaults = ["is", "was", "are", "am"]
    
    def __init__(
            self, 
            text, 
            verb_pct=0.25, 
            noun_pct=0.25, 
            adv_pct=0.25, 
            adj_pct=0.25,
            addl_stop_words=[]
        ) -> None:
        tokens          = word_tokenize(text)
        self.word_count = len(tokens)
        self.tags       = nltk.pos_tag(tokens, tagset = "universal")
        self.tag_counts = Counter([tag[1] for tag in self.tags])
        self.num_nouns  = self.num_of_type(WordType.NOUN, percent=noun_pct)
        self.num_verbs  = self.num_of_type(WordType.VERB, percent=verb_pct)
        self.num_adj    = self.num_of_type(WordType.ADJ, percent=adj_pct)
        self.num_adv    = self.num_of_type(WordType.ADV, percent=adv_pct)
        self.stop_words = self.stop_word_defaults + addl_stop_words

    def madliberate(self):
        return TreebankWordDetokenizer().detokenize(self.replace_tokens())

    def replace_tokens(self):
        if self.word_count < 10:
            return [tag for tag,_ in self.tags]
        return [
            self.to_lib_or_not_to_lib(tag, index) 
            for index,tag in enumerate(self.tags)
            ]
    
    @property
    def noun_pos(self):
        return self.positions_to_replace(WordType.NOUN, self.num_nouns)
    
    @property
    def verb_pos(self):
        return self.positions_to_replace(WordType.VERB, self.num_verbs)

    @property
    def adj_pos(self):
        return self.positions_to_replace(WordType.ADJ, self.num_adj)
    
    @property
    def adv_pos(self):
        return self.positions_to_replace(WordType.ADV, self.num_adv)
    
    def to_lib_or_not_to_lib(self, tag, index):
        if tag[0].lower() in self.stop_words:
            return tag[0]
        if index in self.noun_pos:
            lemma = WNL.lemmatize(tag[0], 'n')
            if tag[0] != lemma:
                return f"{space_token(WordType.PLURAL_NOUN)}"
            else:
                return f"{space_token(WordType.NOUN)}"
        if index in self.verb_pos:
            return f"{space_token(WordType.VERB)}"
        if index in self.adj_pos:
            return f"{space_token(WordType.ADJ)}"
        if index in self.adv_pos:
            return f"{space_token(WordType.ADV)}"
        return tag[0]


    def num_of_type(self, type: WordType, percent=0.25):
        return ceil(self.tag_counts.get(type.name,1) * percent)
    
    def positions_to_replace(self, type: WordType, num_words):
        population = [
            i for i, tag_n_type in enumerate(self.tags) 
            if tag_n_type[1] == type.name
        ]
        if population:
            return choices(
                population,
                k=num_words)
        return []