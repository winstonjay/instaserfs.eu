from django.db.models import Q
import random

from parse_input import sentence_split

from naive_bayes import Mini_Naive_Bayes

from stock_responses import fail_start


search_fail = [
    "I could not find what you were looking for",
    "I wasent sure if you wanted me to find something",
    "I appear to have lost my marbles or something",
    "i'm having some trouble here if you want me to search for something it might help if you put it in quotes"
]

db_fail = [
    "sorry we dont appear to have anything in the system on that",
    "we dont have anything on this, but in the future you will be able to add to my knowledge",
    "these aren't the droids your looking for",
    "I wish i did know something about that"
]

item_fail = [
    "I was not familiar with",
    "I was unable to find you anything concerning",
    "I appear to have lost my marbles or something. What about",
    "I don't appear to have anything on"
]

class Info_Unit(object):

    def __init__(self, db):
        super(Info_Unit, self).__init__()

        self.db = db


    def look_up(self, subjects):

        items = {}
        for sub in (sub for sub in subjects):
            items[sub] = self.db.objects.filter(
                Q(item_title__icontains=sub) |
                Q(item_info__icontains=sub)
            )
            print sub

        if len(items) == 0:
            print 0, items
            return False

        sents = []

        try:
            for key, value in items.items():
                
                value = [sentence_split(str(val.item_info)) for val in value][0]

                for val in value:
                    sents.append(val)


            del items

            response = random.choice(sents)
        except:
            response = "{0} {1} '{2}'.".format(random.choice(fail_start), random.choice(item_fail), subjects[0])

        return response

        # naive = Mini_Naive_Bayes(sents, 1)

        # print naive.probability_dist(sents[0])





    def response(self, sentence, subjects):
        if subjects:
            res = self.look_up(subjects)
            if not res:
                return "{0} {1}".format(random.choice(fail_start), random.choice(db_fail))

            return res
        else:
            return "{0} {1}".format(random.choice(fail_start), random.choice(search_fail))
        




