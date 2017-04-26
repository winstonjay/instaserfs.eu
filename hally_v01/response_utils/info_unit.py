import random




class Info_Unit(object):

    def __init__(self):
        super(Info_Unit, self).__init__()


    def response(self, sentence, subjects):
        if subjects:
            return "I dont know much about %s would you like to add something so i will in the future" % subjects
        else:
            return "oh no"
        

