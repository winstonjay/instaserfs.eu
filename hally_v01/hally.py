import os, random

from sklearn.externals import joblib

from response_utils.parse_input import parse_format_input, switch_possessive
from response_utils.noun_select import Noun_Select

from response_utils.math_unit import Math_Unit
from response_utils.info_unit import Info_Unit


class Hally(object):
    """Hally"""
    def __init__(self):
        super(Hally, self).__init__()


    # load trained sklearn classifier
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

        dispatcher = {
            "MATH": Math_Unit(),
            "SEAR": Info_Unit(),
            "LERN": Info_Unit()
        }

        try: 
            response = dispatcher[intent].response(sent, subjects)
            return response

        except:

            if intent == "POSS":
                return "glad to be of service"

            elif intent == "REMI":
                if subjects:
                    response = "Ok i would remind you about %s" % switch_possessive(subjects)
                else:
                    response = "remind you about what?"
                return response

            else:
                return sent










