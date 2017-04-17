#!/usr/bin/python

import sys, re, pickle
from time import time

from nltk.stem.snowball import SnowballStemmer

sys.path.append( "../" )

from training_data import Training_Data

context_data = []
word_data = []

stemmer = SnowballStemmer("english")


def tokenize(sent):
    return [x.strip() for x in re.split('(\W+)?', sent) if x.strip()]


def parse_out(DATA):
    for context, items in DATA.iteritems():
        print "%s length = %s" % (context, len(items))
        for sentence in items:

            stemmed_words = " ".join([str(stemmer.stem(word)) for word in tokenize(sentence)])

            word_data.append(stemmed_words)

            context_data.append(context)

    print "Total length of words data     = %s" % len(word_data)
    print "Total length of context data   = %s" % len(context_data)

    pickle.dump( context_data, open("../context_data.pkl", "w") )
    pickle.dump( word_data, open("../word_data.pkl", "w") )



print "TRAINING SET INFO:\n"
t0 = time()
parse_out(Training_Data)
print "-" * 40
print "time to complete", round(time()-t0, 3), "s"