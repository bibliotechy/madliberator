from collections import Counter
from math import ceil
from sys import stdin
from random import choices
from typing import List

import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize.treebank import TreebankWordDetokenizer

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')
nltk.download('wordnet')


text = stdin.read()

wnl = WordNetLemmatizer()

tokens = word_tokenize(text)
word_count = len(tokens)
tags = nltk.pos_tag(tokens, tagset = "universal")
tag_counts = Counter([tag[1] for tag in tags])

from enum import Enum

class WordType(Enum):
    NOUN = "NOUN"
    VERB = "VERB"
    ADJ  = "ADJ"
    ADV  = "ADV"

    PLURAL_NOUN = "PLURAL NOUN"


def num_of_type(type: WordType, percent=0.25):
    return ceil(tag_counts.get(type.name,1) * percent)


def positions_to_replace(type: WordType, num_words):
    population = [i for i,tag_n_type in enumerate(tags) if tag_n_type[1] == type.name]
    if population:
        return choices(
            population,
            k=num_words)
    return []

num_nouns = num_of_type(WordType.NOUN)
noun_pos  = positions_to_replace(WordType.NOUN, num_nouns)

num_verbs = num_of_type(WordType.VERB, percent=0.5)
verb_pos  = positions_to_replace(WordType.VERB, num_verbs)

num_adj   = num_of_type(WordType.ADJ)
adj_pos   = positions_to_replace(WordType.ADJ, num_adj)

num_adv   = num_of_type(WordType.ADV)
adv_pos   = positions_to_replace(WordType.ADV, num_adv)

# for tag in tags:
#     if tag[1] == "NOUN":
#         lemma = wnl.lemmatize(tag[0], 'n')
#         if tag[0] != lemma:
#             print(f"{tag[0]} is plural")



def space_token(word_type: WordType):
    return f"{{{{{word_type.name}}}}}"

def madlib(tag, index):
    if index in noun_pos:
        lemma = wnl.lemmatize(tag[0], 'n')
        if tag[0] != lemma:
            return f"{space_token(WordType.PLURAL_NOUN)}"
        else:
            return f"{space_token(WordType.NOUN)}"
    if index in verb_pos:
        return f"{space_token(WordType.VERB)}"
    if index in adj_pos:
        return f"{space_token(WordType.ADJ)}"
    if index in adv_pos:
        return f"{space_token(WordType.ADV)}"
    return tag[0]

madlibified = [madlib(tag, index) for index,tag in enumerate(tags)]

print(TreebankWordDetokenizer().detokenize(madlibified))
