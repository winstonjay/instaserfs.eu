import re

from nltk import RegexpParser as nltk_RegexParser
from nltk import pos_tag as nltk_pos_tag

from bad_words import BAD_WORDS


class NounSelector(object):
    """aids selection of Nouns"""

    def __init__(self):
        super(NounSelector, self).__init__()


    stopwords = BAD_WORDS
    stopwords.append("search")
    stopwords.append("whats")
    stopwords.append("example")

    grammar = r"""
        NBAR:
            {<NN.*|PR.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
            
        NP:
            {<NBAR>}
            {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
    """
    chunker = nltk_RegexParser(grammar)



    def noun_tokenize(self, sent):
        # removes white space but keeps punctuation
        return [x.strip() for x in re.split(r'(\w+[\.*\:*\-*\w*]*\.*\-*\w*)?', sent) if x.strip()]


    def acceptable_word(self, word):
        """Checks conditions for acceptable word: length, stopword."""
        return bool(2 <= len(word) <= 20 and word.lower() not in self.stopwords)


    def get_leaves(self, tree):
        """Finds NP (nounphrase) leaf nodes of a chunk tree."""
        for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
            yield subtree.leaves()


    def get_terms(self, sent):
        """ returns array of noun phrases """
        words = self.noun_tokenize(sent)
        pos_tags = nltk_pos_tag(words)

        tree = self.chunker.parse(pos_tags)

        terms = []
        for leaf in self.get_leaves(tree):
            term = [w for w, t in leaf if self.acceptable_word(w)]
            if len(term) >= 1:
                terms.append(" ".join(term))

        return terms


Noun_Select = NounSelector()





