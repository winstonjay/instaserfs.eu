import os
from sklearn.externals import joblib

from response_utils.parse_input import parse_format_input, switch_possessive
from response_utils.noun_select import Noun_Select
from response_utils.simple_math import Simple_Math



class Hally(object):
    """Hally"""
    def __init__(self):
        super(Hally, self).__init__()


    direct = os.path.dirname(__file__)
    filename = os.path.join(direct, 'data/data_models')

    models = joblib.load(filename)

    def predict_intent(self, sent):
        sent = parse_format_input(sent)
        for name, clf in self.models.iteritems():
            intent = clf.predict(sent)[0]
        return intent


    def predict_subjects(self, sent):

        nouns = Noun_Select.get_terms(sent)

        if len(nouns) <= 0:
            return False
        elif len(nouns) > 1:
            return ", ".join(nouns)
        else:
            return nouns[0]


    def decide_response(self, sent, intent, subjects):

        if intent == "MATH":

            return Simple_Math(sent)

        elif intent == "REMI":
            if subjects:
                response = "Ok i will remind you about %s" % switch_possessive(subjects)
            else:
                response = "remind you about what?"
            return response

        elif intent == "LERN" or intent == "SEAR":
            if subjects:
                return "I dont know much about %s would you like to add something so i will in the future" % subjects
            else:
                return self.decide_response(sent, "RAND", False)

        else:
            return sent










