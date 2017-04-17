#!/usr/bin/python

import re

from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english")

def tokenize(sent):
    # removes white space but keeps punctuation
    return [x.strip() for x in re.split('(\W+)?', sent) if x.strip()]


def parse_format_input(sentence):

    # replace all numbers to match data
    sentence = re.sub(r'(-*[0-9]+\.*[0-9]*)+', 'XNUM', sentence)

    # tokenize, stem words join back together
    sentence = [ str(" ".join( [ stemmer.stem(word) for word in tokenize(sentence) ]) ) ]

    return sentence


def sentence_split(sentence):
    # only splits with dots with a space if and returns if more than 3 words long
    return [x for x in re.split('\. ', sentence) if re.match(r'^(.*\s+.*\s+.*)+$', x)]


def switch_possessive(sentence):

    pairs = {
        "my": "your",
        "your": "my",
        "I": "you",
        "me": "you",
        "you": "me",
        "I am": "you are",
        "you are": "I am",
        "you're": "I am",
        "are you": "am I",
        "am I": "are you"
    }

    new_sentence = []

    for word in sentence.split():
        if word in pairs:
            new_sentence.append(pairs[word])
        else:
            new_sentence.append(word)

    sentence = " ".join(new_sentence)

    return sentence