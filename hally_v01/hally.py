import os, random

from sklearn.externals import joblib

from response_utils.parse_input import parse_format_input
from response_utils.noun_select import Noun_Select

from response_utils.math_unit import Math_Unit
from response_utils.info_unit import Info_Unit
from response_utils.reminder_unit import Reminder_Unit

from response_utils.stock_responses import *

from models import Knowledge

class Hally(object):
    """Hally verson 0"""
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
        print nouns
        if len(nouns) <= 0:
            return False
        else:
            return nouns



    def decide_response(self, sent, intent, subjects):

        dispatcher = {
            "MATH": Math_Unit(),
            "SEAR": Info_Unit(Knowledge),
            "LERN": Info_Unit(Knowledge),
            "REMI": Reminder_Unit()
        }

        try: 
            return dispatcher[intent].response(sent, subjects)

        except:
            if intent == "SEAR":
                return dispatcher[intent].response(sent, subjects)
            
            if intent == "JOKE":
                return random.choice(Jokes)

            if intent == "POSS":
                return "glad to be of service"

            if intent == "NEGG":
                return "{0} is there anything i can do to make this better".format(random.choice(fail_start))
                
                # return dispatcher[intent].response(sent, subjects, intent)

            if intent == "BYES":
                return random.choice(bye_responses)

            if intent == "GRET":
                return random.choice(hey_responses)



            else:
                return sent










